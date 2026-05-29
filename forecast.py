#!/usr/bin/env python3
"""
TimeSeriesForecast - 轻量级时间序列预测CLI工具
零依赖、纯Python标准库实现的时间序列预测工具
"""

import sys
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from models import MovingAverage, ExponentialSmoothing, LinearTrend, SimpleRegression
from utils import DataLoader, DataProcessor, OutputFormatter
from visualization import AsciiChart, ChartGenerator


class TimeSeriesForecaster:
    """时间序列预测器主类"""
    
    MODELS = {
        'sma': MovingAverage,
        'wma': MovingAverage,
        'es': ExponentialSmoothing,
        'lt': LinearTrend,
        'sr': SimpleRegression
    }
    
    def __init__(self):
        self.data = None
        self.model = None
        self.predictions = None
        
    def load_data(self, file_path, date_col=None, value_col=None):
        """加载数据"""
        loader = DataLoader()
        self.data = loader.load(file_path, date_col, value_col)
        return self.data
    
    def preprocess(self, fill_method='linear'):
        """数据预处理"""
        processor = DataProcessor()
        self.data = processor.process(self.data, fill_method)
        return self.data
    
    def train(self, model_type='sma', **kwargs):
        """训练模型"""
        if model_type not in self.MODELS:
            raise ValueError(f"不支持的模型类型: {model_type}. 可选: {', '.join(self.MODELS.keys())}")
        
        model_class = self.MODELS[model_type]
        self.model = model_class(**kwargs)
        self.model.fit(self.data)
        
        return self.model
    
    def predict(self, periods=30):
        """进行预测"""
        if self.model is None:
            raise RuntimeError("请先训练模型")
        
        self.predictions = self.model.predict(periods)
        return self.predictions
    
    def evaluate(self):
        """评估模型"""
        if self.model is None:
            raise ValueError("请先训练模型")
        
        return self.model.evaluate()
    
    def visualize(self, output_type='ascii'):
        """可视化"""
        if output_type == 'ascii':
            chart = AsciiChart()
            return chart.render(self.data, self.predictions)
        else:
            generator = ChartGenerator()
            return generator.render(self.data, self.predictions, output_type)


def create_parser():
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description='TimeSeriesForecast - 轻量级时间序列预测CLI工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s run data.csv --model sma --period 30
  %(prog)s run sales.csv --model es --alpha 0.3 --period 90
  %(prog)s compare data.csv --models sma,es,lt --period 30
  %(prog)s plot data.csv --output forecast.png --period 60
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # run命令
    run_parser = subparsers.add_parser('run', help='运行预测')
    run_parser.add_argument('file', help='数据文件路径 (CSV/JSON)')
    run_parser.add_argument('--model', '-m', default='sma', 
                           choices=['sma', 'wma', 'es', 'lt', 'sr'],
                           help='预测模型 (默认: sma)')
    run_parser.add_argument('--period', '-p', type=int, default=30,
                           help='预测周期数 (默认: 30)')
    run_parser.add_argument('--window', '-w', type=int, default=7,
                           help='移动平均窗口大小 (默认: 7)')
    run_parser.add_argument('--alpha', '-a', type=float, default=0.3,
                           help='指数平滑alpha值 (默认: 0.3)')
    run_parser.add_argument('--date-col', help='日期列名')
    run_parser.add_argument('--value-col', help='数值列名')
    run_parser.add_argument('--no-plot', action='store_true',
                           help='不显示图表')
    run_parser.add_argument('--output', '-o', help='保存结果到文件')
    
    # compare命令
    compare_parser = subparsers.add_parser('compare', help='比较多个模型')
    compare_parser.add_argument('file', help='数据文件路径')
    compare_parser.add_argument('--models', '-m', default='sma,es,lt',
                                help='逗号分隔的模型列表')
    compare_parser.add_argument('--period', '-p', type=int, default=30,
                               help='预测周期数')
    compare_parser.add_argument('--window', '-w', type=int, default=7,
                               help='移动平均窗口大小')
    compare_parser.add_argument('--top-k', type=int, default=3,
                               help='显示前N个最佳模型')
    
    # plot命令
    plot_parser = subparsers.add_parser('plot', help='生成图表')
    plot_parser.add_argument('file', help='数据文件路径')
    plot_parser.add_argument('--output', '-o', default='forecast.png',
                            help='输出文件路径')
    plot_parser.add_argument('--model', '-m', default='sma',
                            choices=['sma', 'wma', 'es', 'lt', 'sr'])
    plot_parser.add_argument('--period', '-p', type=int, default=30)
    plot_parser.add_argument('--width', type=int, default=800,
                            help='图表宽度 (像素)')
    plot_parser.add_argument('--height', type=int, default=600,
                            help='图表高度 (像素)')
    
    # info命令
    info_parser = subparsers.add_parser('info', help='显示模型信息')
    info_parser.add_argument('--model', '-m', 
                            choices=['sma', 'wma', 'es', 'lt', 'sr'],
                            help='指定模型信息')
    
    return parser


def cmd_run(args):
    """处理run命令"""
    forecaster = TimeSeriesForecaster()
    
    # 加载数据
    print(f"📊 加载数据: {args.file}")
    try:
        data = forecaster.load_data(args.file, args.date_col, args.value_col)
        print(f"   成功加载 {len(data)} 条数据")
    except Exception as e:
        print(f"❌ 数据加载失败: {e}")
        return 1
    
    # 预处理
    print("🔧 数据预处理...")
    data = forecaster.preprocess()
    print(f"   处理完成")
    
    # 训练模型
    print(f"🤖 训练模型: {args.model}")
    model_kwargs = {}
    if args.model in ['sma', 'wma']:
        model_kwargs['window'] = args.window
    elif args.model == 'es':
        model_kwargs['alpha'] = args.alpha
    
    try:
        forecaster.train(args.model, **model_kwargs)
        print(f"   模型训练完成")
    except Exception as e:
        print(f"❌ 模型训练失败: {e}")
        return 1
    
    # 预测
    print(f"🔮 预测未来 {args.period} 个周期...")
    predictions = forecaster.predict(args.period)
    print(f"   预测完成")
    
    # 评估
    metrics = forecaster.evaluate()
    print("\n📈 模型评估指标:")
    for metric, value in metrics.items():
        print(f"   {metric}: {value:.4f}")
    
    # 输出预测结果
    print("\n📋 预测结果:")
    formatter = OutputFormatter()
    formatted = formatter.format_predictions(predictions)
    print(formatted)
    
    # 可视化
    if not args.no_plot:
        print("\n📊 预测趋势图:")
        chart = forecaster.visualize('ascii')
        print(chart)
    
    # 保存结果
    if args.output:
        formatter.save_predictions(predictions, args.output)
        print(f"\n💾 预测结果已保存到: {args.output}")
    
    return 0


def cmd_compare(args):
    """处理compare命令"""
    print(f"📊 数据文件: {args.file}")
    print(f"🔄 比较模型: {args.models}\n")
    
    # 加载数据
    loader = DataLoader()
    try:
        data = loader.load(args.file)
        print(f"✅ 加载 {len(data)} 条数据\n")
    except Exception as e:
        print(f"❌ 数据加载失败: {e}")
        return 1
    
    # 预处理
    processor = DataProcessor()
    data = processor.process(data)
    
    # 比较每个模型
    models = args.models.split(',')
    results = []
    
    for model_name in models:
        model_name = model_name.strip()
        if model_name not in TimeSeriesForecaster.MODELS:
            print(f"⚠️ 跳过未知模型: {model_name}")
            continue
        
        try:
            forecaster = TimeSeriesForecaster()
            forecaster.data = data
            model_class = TimeSeriesForecaster.MODELS[model_name]
            model = model_class()
            model.fit(data)
            predictions = model.predict(args.period)
            metrics = model.evaluate()
            
            results.append({
                'name': model_name,
                'metrics': metrics,
                'predictions': predictions
            })
            
            print(f"✅ {model_name}: RMSE={metrics.get('RMSE', 0):.4f}, MAE={metrics.get('MAE', 0):.4f}")
        except Exception as e:
            print(f"❌ {model_name}: 训练失败 - {e}")
    
    # 排序并显示最佳模型
    if results:
        results.sort(key=lambda x: x['metrics'].get('RMSE', float('inf')))
        
        print("\n🏆 模型排名 (按RMSE):")
        for i, result in enumerate(results[:args.top_k], 1):
            print(f"   {i}. {result['name']} - RMSE: {result['metrics'].get('RMSE', 0):.4f}")
        
        # 显示最佳模型的预测
        print(f"\n📊 最佳模型 ({results[0]['name']}) 预测结果:")
        formatter = OutputFormatter()
        print(formatter.format_predictions(results[0]['predictions']))
    
    return 0


def cmd_plot(args):
    """处理plot命令"""
    print(f"📊 生成图表: {args.file}")
    print(f"📈 输出文件: {args.output}")
    
    # 加载和预处理数据
    forecaster = TimeSeriesForecaster()
    try:
        data = forecaster.load_data(args.file)
        data = forecaster.preprocess()
    except Exception as e:
        print(f"❌ 数据处理失败: {e}")
        return 1
    
    # 训练和预测
    try:
        forecaster.train(args.model)
        predictions = forecaster.predict(args.period)
    except Exception as e:
        print(f"❌ 预测失败: {e}")
        return 1
    
    # 生成图表
    generator = ChartGenerator()
    try:
        generator.render(data, predictions, args.output, args.width, args.height)
        print(f"✅ 图表已保存到: {args.output}")
    except ImportError:
        print("⚠️ Matplotlib未安装，使用ASCII图表:")
        chart = AsciiChart()
        print(chart.render(data, predictions))
    except Exception as e:
        print(f"❌ 图表生成失败: {e}")
        return 1
    
    return 0


def cmd_info(args):
    """处理info命令"""
    if args.model:
        models = [args.model]
    else:
        models = ['sma', 'wma', 'es', 'lt', 'sr']
    
    print("📚 TimeSeriesForecast 支持的模型:\n")
    
    model_info = {
        'sma': ('简单移动平均', 'Simple Moving Average', '短期平滑、快速、对噪声敏感'),
        'wma': ('加权移动平均', 'Weighted Moving Average', '可调权重、趋势跟随'),
        'es': ('指数平滑', 'Exponential Smoothing', '考虑历史权重、中期预测'),
        'lt': ('线性趋势', 'Linear Trend', '线性增长数据、简单直观'),
        'sr': ('简单回归', 'Simple Regression', '关系预测、可处理多特征')
    }
    
    for model in models:
        if model in model_info:
            cn_name, en_name, desc = model_info[model]
            print(f"  {model.upper()} - {cn_name} ({en_name})")
            print(f"    特点: {desc}\n")
    
    return 0


def main():
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    # 执行对应命令
    commands = {
        'run': cmd_run,
        'compare': cmd_compare,
        'plot': cmd_plot,
        'info': cmd_info
    }
    
    if args.command in commands:
        try:
            return commands[args.command](args)
        except KeyboardInterrupt:
            print("\n\n⚠️ 操作已取消")
            return 130
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            import traceback
            if '--debug' in sys.argv:
                traceback.print_exc()
            return 1
    else:
        parser.print_help()
        return 0


if __name__ == '__main__':
    sys.exit(main())
