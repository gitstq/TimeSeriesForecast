"""
Matplotlib图表生成器
生成高质量的时间序列预测图表

注意：这是一个可选模块，需要安装matplotlib
如果没有安装matplotlib，将自动降级到ASCII图表
"""

from typing import List, Dict, Any, Optional
from pathlib import Path


class ChartGenerator:
    """
    Matplotlib图表生成器
    
    生成PNG、SVG、PDF等格式的预测图表
    
    参数:
        style: 图表样式 ('default', 'seaborn', 'ggplot', 'dark_background')
        dpi: 图片分辨率
    """
    
    def __init__(self, 
                 style: str = 'default',
                 dpi: int = 100):
        self.style = style
        self.dpi = dpi
        self._mpl_available = None
        
    def _check_matplotlib(self) -> bool:
        """检查matplotlib是否可用"""
        if self._mpl_available is None:
            try:
                import matplotlib
                import matplotlib.pyplot as plt
                import numpy as np
                self._mpl_available = True
                self._plt = plt
                self._np = np
            except ImportError:
                self._mpl_available = False
        
        return self._mpl_available
    
    def render(self, 
               data: List[Dict[str, Any]], 
               predictions: Optional[List[Dict[str, Any]]],
               output_path: str,
               width: int = 800,
               height: int = 600):
        """
        生成预测图表
        
        Args:
            data: 历史数据
            predictions: 预测数据
            output_path: 输出文件路径
            width: 图表宽度（像素）
            height: 图表高度（像素）
        
        Raises:
            ImportError: 如果matplotlib未安装
        """
        if not self._check_matplotlib():
            raise ImportError(
                "Matplotlib未安装。\n"
                "请使用以下命令安装：pip install matplotlib\n"
                "或者使用ASCII图表：forecast run data.csv --no-plot"
            )
        
        plt = self._plt
        np = self._np
        
        # 设置样式
        if self.style != 'default':
            try:
                plt.style.use(self.style)
            except:
                pass
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
        
        # 计算像素到英寸的转换 (默认100 DPI)
        width_inch = width / self.dpi
        height_inch = height / self.dpi
        fig.set_size_inches(width_inch, height_inch)
        
        # 准备数据
        history_x = list(range(len(data)))
        history_y = [d['value'] for d in data]
        
        # 绘制历史数据
        ax.plot(history_x, history_y, 'b-', linewidth=2, label='历史数据', marker='o', markersize=3)
        
        # 绘制预测数据
        if predictions:
            pred_x = list(range(len(data), len(data) + len(predictions)))
            pred_y = [p['value'] for p in predictions]
            lower_y = [p['lower'] for p in predictions]
            upper_y = [p['upper'] for p in predictions]
            
            # 预测线
            ax.plot(pred_x, pred_y, 'r--', linewidth=2, label='预测值', marker='s', markersize=3)
            
            # 置信区间
            ax.fill_between(pred_x, lower_y, upper_y, alpha=0.3, color='red', label='95% 置信区间')
        
        # 设置标题和标签
        ax.set_title('时间序列预测', fontsize=14, fontweight='bold')
        ax.set_xlabel('时间周期', fontsize=12)
        ax.set_ylabel('数值', fontsize=12)
        
        # 添加网格
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # 添加图例
        ax.legend(loc='best', fontsize=10)
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图表
        output_path = Path(output_path)
        
        try:
            # 根据扩展名确定格式
            format = output_path.suffix.lstrip('.').lower()
            
            if format == 'jpg':
                format = 'jpeg'
            
            plt.savefig(output_path, dpi=self.dpi, format=format)
            print(f"✅ 图表已保存到: {output_path}")
        except Exception as e:
            print(f"❌ 保存图表失败: {e}")
            # 尝试保存为PNG
            png_path = output_path.with_suffix('.png')
            plt.savefig(png_path, dpi=self.dpi, format='png')
            print(f"   已保存为PNG格式: {png_path}")
        finally:
            plt.close()
    
    def render_multi_model(self,
                          data: List[Dict[str, Any]],
                          predictions_dict: Dict[str, List[Dict[str, Any]]],
                          output_path: str,
                          width: int = 800,
                          height: int = 600):
        """
        渲染多模型对比图
        
        Args:
            data: 历史数据
            predictions_dict: {模型名: 预测结果} 的字典
            output_path: 输出文件路径
            width: 图表宽度
            height: 图表高度
        """
        if not self._check_matplotlib():
            raise ImportError("Matplotlib未安装")
        
        plt = self._plt
        np = self._np
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
        
        # 绘制历史数据
        history_x = list(range(len(data)))
        history_y = [d['value'] for d in data]
        ax.plot(history_x, history_y, 'k-', linewidth=2, label='历史数据')
        
        # 绘制各模型的预测
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        
        for i, (model_name, predictions) in enumerate(predictions_dict.items()):
            if not predictions:
                continue
            
            pred_x = list(range(len(data), len(data) + len(predictions)))
            pred_y = [p['value'] for p in predictions]
            
            color = colors[i % len(colors)]
            ax.plot(pred_x, pred_y, '--', color=color, linewidth=2, label=model_name)
        
        # 设置标题和标签
        ax.set_title('多模型预测对比', fontsize=14, fontweight='bold')
        ax.set_xlabel('时间周期', fontsize=12)
        ax.set_ylabel('数值', fontsize=12)
        
        # 添加网格和图例
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(loc='best', fontsize=10)
        
        # 保存图表
        plt.tight_layout()
        
        output_path = Path(output_path)
        plt.savefig(output_path, dpi=self.dpi)
        plt.close()
        
        print(f"✅ 对比图已保存到: {output_path}")
    
    def render_components(self,
                         data: List[Dict[str, Any]],
                         trend: List[float],
                         seasonal: Optional[List[float]],
                         residual: List[float],
                         output_path: str):
        """
        渲染时间序列分解图
        
        Args:
            data: 原始数据
            trend: 趋势分量
            seasonal: 季节性分量
            residual: 残差分量
            output_path: 输出文件路径
        """
        if not self._check_matplotlib():
            raise ImportError("Matplotlib未安装")
        
        plt = self._plt
        
        # 创建子图
        if seasonal is not None:
            fig, axes = plt.subplots(4, 1, figsize=(10, 8))
        else:
            fig, axes = plt.subplots(3, 1, figsize=(10, 6))
        
        # 原始数据
        axes[0].plot([d['value'] for d in data], 'b-')
        axes[0].set_title('原始时间序列', fontsize=12)
        axes[0].grid(True, alpha=0.3)
        
        # 趋势
        axes[1].plot(trend, 'r-')
        axes[1].set_title('趋势分量', fontsize=12)
        axes[1].grid(True, alpha=0.3)
        
        # 季节性
        if seasonal is not None:
            axes[2].plot(seasonal, 'g-')
            axes[2].set_title('季节性分量', fontsize=12)
            axes[2].grid(True, alpha=0.3)
        
        # 残差
        if seasonal is not None:
            axes[3].plot(residual, 'purple')
            axes[3].set_title('残差', fontsize=12)
            axes[3].grid(True, alpha=0.3)
        else:
            axes[2].plot(residual, 'purple')
            axes[2].set_title('残差', fontsize=12)
            axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        output_path = Path(output_path)
        plt.savefig(output_path, dpi=self.dpi)
        plt.close()
        
        print(f"✅ 分解图已保存到: {output_path}")
