"""
时间序列预测模型基类
定义所有模型的公共接口
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import math


class BaseModel(ABC):
    """时间序列预测模型基类"""
    
    def __init__(self):
        self.data = None
        self.params = {}
        self.is_fitted = False
        
    @abstractmethod
    def fit(self, data: List[Dict[str, Any]]) -> 'BaseModel':
        """
        训练模型
        
        Args:
            data: 时间序列数据，格式为 [{'date': '2024-01-01', 'value': 100}, ...]
        
        Returns:
            self: 返回训练后的模型实例
        """
        pass
    
    @abstractmethod
    def predict(self, periods: int = 30) -> List[Dict[str, Any]]:
        """
        进行预测
        
        Args:
            periods: 预测周期数
        
        Returns:
            预测结果，格式为 [{'date': '2024-02-01', 'value': 105.5, 'lower': 100.2, 'upper': 110.8}, ...]
        """
        pass
    
    def evaluate(self) -> Dict[str, float]:
        """
        评估模型性能
        
        Returns:
            评估指标字典，包含 RMSE, MAE, MAPE 等
        """
        if not self.is_fitted or self.data is None:
            return {'RMSE': 0.0, 'MAE': 0.0, 'MAPE': 0.0}
        
        values = [d['value'] for d in self.data]
        predictions = self._get_fitted_values()
        
        # 计算评估指标
        n = len(values)
        
        # RMSE
        squared_errors = [(values[i] - predictions[i]) ** 2 for i in range(n)]
        rmse = math.sqrt(sum(squared_errors) / n)
        
        # MAE
        abs_errors = [abs(values[i] - predictions[i]) for i in range(n)]
        mae = sum(abs_errors) / n
        
        # MAPE
        non_zero_values = [values[i] for i in range(n) if values[i] != 0]
        if non_zero_values:
           ape = [abs(values[i] - predictions[i]) / values[i] * 100 
                   for i in range(n) if values[i] != 0]
            mape = sum(ape) / len(ape)
        else:
            mape = 0.0
        
        return {
            'RMSE': rmse,
            'MAE': mae,
            'MAPE': mape
        }
    
    @abstractmethod
    def _get_fitted_values(self) -> List[float]:
        """获取模型在训练数据上的拟合值"""
        pass
    
    def _calculate_confidence_interval(self, 
                                       prediction: float, 
                                       std_error: float, 
                                       confidence: float = 0.95) -> tuple:
        """
        计算置信区间
        
        Args:
            prediction: 预测值
            std_error: 标准误差
            confidence: 置信水平
        
        Returns:
            (lower, upper): 置信区间下限和上限
        """
        # Z分数表
        z_scores = {
            0.90: 1.645,
            0.95: 1.96,
            0.99: 2.576
        }
        
        z = z_scores.get(confidence, 1.96)
        margin = z * std_error
        
        return (prediction - margin, prediction + margin)
    
    def _get_last_date(self) -> str:
        """获取最后一条数据的日期"""
        if not self.data:
            return None
        return self.data[-1]['date']
    
    def _parse_date(self, date_str: str) -> str:
        """
        解析日期字符串，返回标准格式
        实际实现应该更复杂，这里简化处理
        """
        return date_str
    
    def get_params(self) -> Dict[str, Any]:
        """获取模型参数"""
        return self.params.copy()
    
    def set_params(self, **params):
        """设置模型参数"""
        self.params.update(params)
        return self
