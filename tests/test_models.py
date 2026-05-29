"""
TimeSeriesForecast 单元测试
测试核心模型和工具模块
"""

import unittest
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import MovingAverage, ExponentialSmoothing, LinearTrend, SimpleRegression
from utils import DataLoader, DataProcessor, OutputFormatter
from visualization import AsciiChart


class TestModels(unittest.TestCase):
    """测试预测模型"""
    
    def setUp(self):
        """准备测试数据"""
        self.test_data = [
            {'date': '2024-01-01', 'value': 100},
            {'date': '2024-01-02', 'value': 110},
            {'date': '2024-01-03', 'value': 105},
            {'date': '2024-01-04', 'value': 115},
            {'date': '2024-01-05', 'value': 120},
            {'date': '2024-01-06', 'value': 118},
            {'date': '2024-01-07', 'value': 125},
        ]
    
    def test_moving_average(self):
        """测试简单移动平均模型"""
        model = MovingAverage(window=3)
        model.fit(self.test_data)
        predictions = model.predict(periods=3)
        
        self.assertEqual(len(predictions), 3)
        self.assertIn('value', predictions[0])
        self.assertIn('lower', predictions[0])
        self.assertIn('upper', predictions[0])
        
        # 验证评估指标
        metrics = model.evaluate()
        self.assertIn('RMSE', metrics)
        self.assertIn('MAE', metrics)
        self.assertIn('MAPE', metrics)
    
    def test_exponential_smoothing(self):
        """测试指数平滑模型"""
        model = ExponentialSmoothing(alpha=0.3)
        model.fit(self.test_data)
        predictions = model.predict(periods=3)
        
        self.assertEqual(len(predictions), 3)
        self.assertTrue(all('value' in p for p in predictions))
    
    def test_linear_trend(self):
        """测试线性趋势模型"""
        model = LinearTrend()
        model.fit(self.test_data)
        predictions = model.predict(periods=3)
        
        self.assertEqual(len(predictions), 3)
        
        # 检查趋势信息
        trend_info = model.get_trend_info()
        self.assertIn('slope', trend_info)
        self.assertIn('direction', trend_info)
    
    def test_simple_regression(self):
        """测试简单回归模型"""
        model = SimpleRegression(max_degree=2)
        model.fit(self.test_data)
        predictions = model.predict(periods=3)
        
        self.assertEqual(len(predictions), 3)


class TestDataLoader(unittest.TestCase):
    """测试数据加载器"""
    
    def test_from_list(self):
        """测试从列表创建数据"""
        loader = DataLoader()
        values = [100, 110, 120, 130]
        data = loader.from_list(values)
        
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0]['value'], 100)
        self.assertEqual(data[1]['value'], 110)
    
    def test_from_dict(self):
        """测试从字典创建数据"""
        loader = DataLoader()
        data_dict = {
            '2024-01-01': 100,
            '2024-01-02': 110,
            '2024-01-03': 120
        }
        data = loader.from_dict(data_dict)
        
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['date'], '2024-01-01')
        self.assertEqual(data[0]['value'], 100)


class TestDataProcessor(unittest.TestCase):
    """测试数据处理器"""
    
    def setUp(self):
        """准备测试数据"""
        self.test_data = [
            {'date': '2024-01-01', 'value': 100},
            {'date': '2024-01-02', 'value': 110},
            {'date': '2024-01-03', 'value': None},  # 缺失值
            {'date': '2024-01-04', 'value': 115},
            {'date': '2024-01-05', 'value': 120},
        ]
    
    def test_handle_missing_linear(self):
        """测试线性插值填充缺失值"""
        processor = DataProcessor()
        result = processor.process(self.test_data, fill_method='linear')
        
        # 检查缺失值是否被填充
        self.assertIsNotNone(result[2]['value'])
        self.assertTrue(100 <= result[2]['value'] <= 120)
    
    def test_handle_missing_mean(self):
        """测试均值填充"""
        processor = DataProcessor()
        result = processor.process(self.test_data, fill_method='mean')
        
        # 检查填充值是否为均值
        valid_values = [100, 110, 115, 120]
        expected_mean = sum(valid_values) / len(valid_values)
        self.assertAlmostEqual(result[2]['value'], expected_mean)
    
    def test_statistics(self):
        """测试统计信息计算"""
        processor = DataProcessor()
        data = [
            {'date': '2024-01-01', 'value': 100},
            {'date': '2024-01-02', 'value': 110},
            {'date': '2024-01-03', 'value': 120},
        ]
        
        processor.process(data)
        stats = processor.get_statistics()
        
        self.assertEqual(stats['count'], 3)
        self.assertEqual(stats['mean'], 110)
        self.assertEqual(stats['min'], 100)
        self.assertEqual(stats['max'], 120)


class TestOutputFormatter(unittest.TestCase):
    """测试输出格式化器"""
    
    def test_format_predictions_table(self):
        """测试表格格式输出"""
        predictions = [
            {'period': 1, 'value': 100.5, 'lower': 95.0, 'upper': 106.0},
            {'period': 2, 'value': 102.0, 'lower': 96.5, 'upper': 107.5},
        ]
        
        formatter = OutputFormatter()
        result = formatter.format_predictions(predictions, format='table')
        
        self.assertIn('周期', result)
        self.assertIn('预测值', result)
    
    def test_format_predictions_json(self):
        """测试JSON格式输出"""
        predictions = [
            {'period': 1, 'value': 100.5, 'lower': 95.0, 'upper': 106.0},
        ]
        
        formatter = OutputFormatter()
        result = formatter.format_predictions(predictions, format='json')
        
        self.assertIn('"period": 1', result)
        self.assertIn('"value": 100.5', result)
    
    def test_format_metrics(self):
        """测试指标格式化"""
        metrics = {
            'RMSE': 10.5,
            'MAE': 8.2,
            'MAPE': 5.5
        }
        
        formatter = OutputFormatter()
        result = formatter.format_metrics(metrics)
        
        self.assertIn('RMSE', result)
        self.assertIn('10.50', result)


class TestAsciiChart(unittest.TestCase):
    """测试ASCII图表生成器"""
    
    def test_render(self):
        """测试图表渲染"""
        data = [
            {'date': '2024-01-01', 'value': 100},
            {'date': '2024-01-02', 'value': 110},
            {'date': '2024-01-03', 'value': 105},
        ]
        
        chart = AsciiChart(width=40, height=10)
        result = chart.render(data)
        
        self.assertIn('时间序列趋势图', result)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)


def run_tests():
    """运行所有测试"""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    run_tests()
