"""
简单移动平均 (Simple Moving Average) 和加权移动平均 (Weighted Moving Average) 模型
"""

from typing import List, Dict, Any
from .base import BaseModel


class MovingAverage(BaseModel):
    """
    移动平均模型
    
    支持简单移动平均 (SMA) 和加权移动平均 (WMA)
    
    参数:
        window: 移动窗口大小，默认7
        weighted: 是否使用加权，默认为False（简单移动平均）
    """
    
    def __init__(self, window: int = 7, weighted: bool = False):
        super().__init__()
        self.window = window
        self.weighted = weighted
        self.params = {
            'window': window,
            'weighted': weighted
        }
        
    def fit(self, data: List[Dict[str, Any]]) -> 'MovingAverage':
        """
        训练移动平均模型
        
        Args:
            data: 时间序列数据
        
        Returns:
            self
        """
        self.data = data
        self.is_fitted = True
        return self
    
    def predict(self, periods: int = 30) -> List[Dict[str, Any]]:
        """
        使用移动平均进行预测
        
        Args:
            periods: 预测周期数
        
        Returns:
            预测结果列表
        """
        if not self.is_fitted or self.data is None:
            raise ValueError("模型未训练，请先调用fit()方法")
        
        values = [d['value'] for d in self.data]
        n = len(values)
        
        # 计算移动平均值
        if n < self.window:
            raise ValueError(f"数据量 ({n}) 少于窗口大小 ({self.window})")
        
        # 计算最后一个窗口的移动平均值
        last_window = values[-self.window:]
        
        if self.weighted:
            # 加权移动平均
            weights = list(range(1, self.window + 1))
            sum_weights = sum(weights)
            forecast = sum(w * v for w, v in zip(weights, last_window)) / sum_weights
        else:
            # 简单移动平均
            forecast = sum(last_window) / self.window
        
        # 计算标准误差用于置信区间
        fitted = self._get_fitted_values()
        residuals = [values[i] - fitted[i] for i in range(len(values))]
        std_error = (sum(r**2 for r in residuals) / len(residuals)) ** 0.5
        
        # 生成预测结果
        predictions = []
        last_date = self._get_last_date()
        
        for i in range(1, periods + 1):
            # 预测值（简化处理，使用相同的预测值）
            # 实际应用中可能需要考虑趋势调整
            pred_value = forecast
            
            # 置信区间随预测周期扩大
            interval = std_error * (1 + i / self.window) ** 0.5
            lower = pred_value - 1.96 * interval
            upper = pred_value + 1.96 * interval
            
            predictions.append({
                'period': i,
                'value': pred_value,
                'lower': max(0, lower),  # 确保非负
                'upper': upper
            })
        
        return predictions
    
    def _get_fitted_values(self) -> List[float]:
        """
        获取模型在训练数据上的拟合值
        
        对于移动平均，每个点的拟合值就是该点对应窗口的移动平均值
        """
        if not self.data:
            return []
        
        values = [d['value'] for d in self.data]
        n = len(values)
        
        fitted = []
        for i in range(n):
            if i < self.window - 1:
                # 窗口不足，使用已知数据的均值
                fitted.append(sum(values[:i+1]) / (i + 1))
            else:
                # 标准的移动平均
                window_values = values[i - self.window + 1:i + 1]
                fitted.append(sum(window_values) / self.window)
        
        return fitted


# 别名
WMA = MovingAverage
SMA = MovingAverage
