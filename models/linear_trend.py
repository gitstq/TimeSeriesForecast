"""
线性趋势 (Linear Trend) 模型
"""

from typing import List, Dict, Any
from .base import BaseModel


class LinearTrend(BaseModel):
    """
    线性趋势模型
    
    使用最小二乘法拟合时间序列的线性趋势
    y = a + b * t
    
    其中:
        a: 截距（基线值）
        b: 斜率（趋势变化率）
    
    适用于具有明显线性增长或下降趋势的数据
    """
    
    def __init__(self):
        super().__init__()
        self.slope = None
        self.intercept = None
        
    def fit(self, data: List[Dict[str, Any]]) -> 'LinearTrend':
        """
        训练线性趋势模型
        
        使用最小二乘法 (OLS) 拟合线性趋势
        
        Args:
            data: 时间序列数据
        
        Returns:
            self
        """
        self.data = data
        n = len(data)
        
        if n < 2:
            raise ValueError("数据点至少需要2个")
        
        # 提取数值
        values = [d['value'] for d in data]
        
        # 创建时间索引 (0, 1, 2, ..., n-1)
        t = list(range(n))
        
        # 计算均值
        t_mean = sum(t) / n
        y_mean = sum(values) / n
        
        # 计算斜率和截距
        # b = Σ((t_i - t_mean) * (y_i - y_mean)) / Σ((t_i - t_mean)^2)
        numerator = sum((t[i] - t_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((t[i] - t_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            raise ValueError("无法拟合线性趋势（所有数据点相同）")
        
        self.slope = numerator / denominator
        self.intercept = y_mean - self.slope * t_mean
        
        self.is_fitted = True
        return self
    
    def predict(self, periods: int = 30) -> List[Dict[str, Any]]:
        """
        使用线性趋势进行预测
        
        Args:
            periods: 预测周期数
        
        Returns:
            预测结果列表
        """
        if not self.is_fitted or self.data is None:
            raise ValueError("模型未训练，请先调用fit()方法")
        
        n = len(self.data)
        
        # 计算残差用于置信区间
        values = [d['value'] for d in self.data]
        fitted = self._get_fitted_values()
        residuals = [values[i] - fitted[i] for i in range(n)]
        
        # 残差标准误差
        std_error = (sum(r**2 for r in residuals) / max(1, n - 2)) ** 0.5
        
        # 生成预测
        predictions = []
        
        for i in range(1, periods + 1):
            # 预测时间索引
            t = n - 1 + i
            
            # 线性预测: y = intercept + slope * t
            pred_value = self.intercept + self.slope * t
            
            # 置信区间随预测周期扩大
            # 使用预测标准误差的扩展公式
            se = std_error * (1 + 1/n + (t - (n-1)/2)**2 / sum((j - (n-1)/2)**2 for j in range(n))) ** 0.5
            
            lower = pred_value - 1.96 * se
            upper = pred_value + 1.96 * se
            
            predictions.append({
                'period': i,
                'value': pred_value,
                'lower': lower,
                'upper': upper
            })
        
        return predictions
    
    def _get_fitted_values(self) -> List[float]:
        """获取拟合值"""
        if not self.data:
            return []
        
        n = len(self.data)
        fitted = []
        
        for t in range(n):
            fitted.append(self.intercept + self.slope * t)
        
        return fitted
    
    def get_trend_info(self) -> Dict[str, Any]:
        """
        获取趋势信息
        
        Returns:
            包含斜率、截距和趋势描述的字典
        """
        if not self.is_fitted:
            return {}
        
        # 判断趋势方向
        if self.slope > 0.01:
            direction = "上升 📈"
        elif self.slope < -0.01:
            direction = "下降 📉"
        else:
            direction = "平稳 ➡️"
        
        return {
            'slope': self.slope,
            'intercept': self.intercept,
            'direction': direction,
            'description': f"每周期{'增加' if self.slope > 0 else '减少'} {abs(self.slope):.2f} 单位"
        }


# 别名
LT = LinearTrend
LinearRegression = LinearTrend
