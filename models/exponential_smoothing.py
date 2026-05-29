"""
指数平滑 (Exponential Smoothing) 模型
"""

from typing import List, Dict, Any
from .base import BaseModel


class ExponentialSmoothing(BaseModel):
    """
    简单指数平滑模型 (Simple Exponential Smoothing)
    
    适用于没有明显趋势和季节性的平稳时间序列
    
    参数:
        alpha: 平滑系数，取值范围 [0, 1]，值越大越重视近期数据
              默认 0.3
        seasonal: 是否使用季节性指数平滑，默认为False
        period: 季节周期，如 7（周）、12（月）
    """
    
    def __init__(self, alpha: float = 0.3, seasonal: bool = False, period: int = 7):
        super().__init__()
        if not 0 <= alpha <= 1:
            raise ValueError("alpha必须在0和1之间")
        
        self.alpha = alpha
        self.seasonal = seasonal
        self.period = period
        self.level = None
        self.seasonal_factors = None
        
        self.params = {
            'alpha': alpha,
            'seasonal': seasonal,
            'period': period
        }
        
    def fit(self, data: List[Dict[str, Any]]) -> 'ExponentialSmoothing':
        """
        训练指数平滑模型
        
        Args:
            data: 时间序列数据
        
        Returns:
            self
        """
        self.data = data
        values = [d['value'] for d in data]
        
        if self.seasonal:
            self._fit_seasonal(values)
        else:
            self._fit_simple(values)
        
        self.is_fitted = True
        return self
    
    def _fit_simple(self, values: List[float]):
        """
        简单指数平滑拟合
        
        递推公式: S_t = α * y_t + (1 - α) * S_{t-1}
        """
        n = len(values)
        
        if n == 0:
            raise ValueError("数据不能为空")
        
        # 初始化：使用第一个观测值
        self.level = values[0]
        
        # 递推计算所有平滑值
        for t in range(1, n):
            self.level = self.alpha * values[t] + (1 - self.alpha) * self.level
    
    def _fit_seasonal(self, values: List[float]):
        """
        季节性指数平滑拟合 (Holt-Winters方法)
        
        使用加法季节性模型
        """
        n = len(values)
        
        if n < 2 * self.period:
            raise ValueError(f"季节性数据需要至少2个完整周期 (2*{self.period}={2*self.period})")
        
        # 初始化水平和平滑因子
        self.level = sum(values[:self.period]) / self.period
        self.seasonal_factors = [0.0] * self.period
        
        # 计算初始季节因子
        for j in range(self.period):
            avg = sum(values[j + i * self.period] for i in range(int(n / self.period))) / int(n / self.period)
            self.seasonal_factors[j] = values[j] - avg
        
        # 递推更新
        for t in range(self.period, n):
            # 去除季节性
            seasonally_adjusted = values[t] - self.seasonal_factors[t % self.period]
            # 更新水平
            self.level = self.alpha * seasonally_adjusted + (1 - self.alpha) * self.level
            # 更新季节因子
            self.seasonal_factors[t % self.period] = (
                self.alpha * (values[t] - self.level) + 
                (1 - self.alpha) * self.seasonal_factors[t % self.period]
            )
    
    def predict(self, periods: int = 30) -> List[Dict[str, Any]]:
        """
        使用指数平滑进行预测
        
        Args:
            periods: 预测周期数
        
        Returns:
            预测结果列表
        """
        if not self.is_fitted or self.data is None:
            raise ValueError("模型未训练，请先调用fit()方法")
        
        values = [d['value'] for d in self.data]
        n = len(values)
        
        # 计算残差用于置信区间
        fitted = self._get_fitted_values()
        residuals = [values[i] - fitted[i] for i in range(n)]
        std_error = (sum(r**2 for r in residuals) / max(1, n - 1)) ** 0.5
        
        # 生成预测
        predictions = []
        
        for i in range(1, periods + 1):
            if self.seasonal and self.seasonal_factors:
                # 季节性预测
                season_idx = (n + i - 1) % self.period
                pred_value = self.level + self.seasonal_factors[season_idx]
            else:
                # 非季节性预测
                pred_value = self.level
            
            # 置信区间
            interval = std_error * (1 + i / 10) ** 0.5
            lower = pred_value - 1.96 * interval
            upper = pred_value + 1.96 * interval
            
            predictions.append({
                'period': i,
                'value': pred_value,
                'lower': max(0, lower),
                'upper': upper
            })
        
        return predictions
    
    def _get_fitted_values(self) -> List[float]:
        """获取拟合值"""
        if not self.data:
            return []
        
        values = [d['value'] for d in self.data]
        n = len(values)
        
        fitted = []
        
        for t in range(n):
            if self.seasonal and self.seasonal_factors:
                # 季节性模型的拟合值
                fitted.append(self.level + self.seasonal_factors[t % self.period])
            else:
                # 简单指数平滑：使用递推公式反向计算
                if t == 0:
                    fitted.append(values[0])
                else:
                    # 简化处理，使用平滑值作为拟合值
                    fitted.append(self.level)
        
        return fitted


# 别名
ES = ExponentialSmoothing
SES = ExponentialSmoothing
