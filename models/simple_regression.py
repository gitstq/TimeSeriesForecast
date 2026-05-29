"""
简单回归 (Simple Regression) 模型
"""

from typing import List, Dict, Any
from .base import BaseModel


class SimpleRegression(BaseModel):
    """
    简单回归模型
    
    基于线性回归的时间序列预测，支持多特征回归
    
    模型: y = β₀ + β₁*x₁ + β₂*x₂ + ... + ε
    
    参数:
        max_degree: 多项式拟合的最高次数，默认1（线性）
        include_trend: 是否包含时间趋势特征，默认True
        include_seasonality: 是否包含季节性特征，默认False
        period: 季节周期（当include_seasonality=True时使用）
    """
    
    def __init__(self, 
                 max_degree: int = 1, 
                 include_trend: bool = True,
                 include_seasonality: bool = False,
                 period: int = 7):
        super().__init__()
        
        if max_degree < 1:
            raise ValueError("max_degree必须 >= 1")
        
        self.max_degree = max_degree
        self.include_trend = include_trend
        self.include_seasonality = include_seasonality
        self.period = period
        
        self.coefficients = []
        
        self.params = {
            'max_degree': max_degree,
            'include_trend': include_trend,
            'include_seasonality': include_seasonality,
            'period': period
        }
        
    def fit(self, data: List[Dict[str, Any]]) -> 'SimpleRegression':
        """
        训练简单回归模型
        
        使用正规方程求解线性回归参数
        
        Args:
            data: 时间序列数据
        
        Returns:
            self
        """
        self.data = data
        n = len(data)
        
        if n < 3:
            raise ValueError("数据点至少需要3个")
        
        # 构建特征矩阵
        X, feature_names = self._build_features(n)
        
        # 提取目标变量
        y = [d['value'] for d in data]
        
        # 使用正规方程求解: θ = (X^T * X)^(-1) * X^T * y
        self.coefficients = self._solve_normal_equation(X, y)
        
        self.is_fitted = True
        return self
    
    def _build_features(self, n: int) -> tuple:
        """
        构建特征矩阵
        
        Returns:
            (X, feature_names): 特征矩阵和特征名称列表
        """
        features = []
        feature_names = []
        
        # 偏置项 (intercept)
        features.append([1.0] * n)
        feature_names.append('bias')
        
        # 多项式特征
        for d in range(1, self.max_degree + 1):
            features.append([(i ** d) for i in range(n)])
            feature_names.append(f't^{d}')
        
        # 时间趋势特征
        if self.include_trend:
            features.append([i for i in range(n)])
            feature_names.append('trend')
            
            # 添加二次趋势
            if self.max_degree >= 2:
                features.append([(i ** 2) for i in range(n)])
                feature_names.append('trend^2')
        
        # 季节性特征
        if self.include_seasonality:
            for k in range(1, min(4, self.period)):  # 最多添加4个季节性谐波
                features.append([self._sin(i, self.period, k) for i in range(n)])
                feature_names.append(f'sin_{k}')
                
                features.append([self._cos(i, self.period, k) for i in range(n)])
                feature_names.append(f'cos_{k}')
        
        # 转置：每列一个特征
        X = [[features[f][i] for f in range(len(features))] for i in range(n)]
        
        return X, feature_names
    
    def _sin(self, t: int, period: int, k: int) -> float:
        """计算正弦季节性特征"""
        import math
        return math.sin(2 * math.pi * k * t / period)
    
    def _cos(self, t: int, period: int, k: int) -> float:
        """计算余弦季节性特征"""
        import math
        return math.cos(2 * math.pi * k * t / period)
    
    def _solve_normal_equation(self, X: List[List[float]], y: List[float]) -> List[float]:
        """
        使用正规方程求解线性回归参数
        
        θ = (X^T * X)^(-1) * X^T * y
        
        注意：这是一个简化实现，使用 NumPy 风格的手动计算
        实际应用中建议使用 NumPy 或其他数值计算库
        """
        import math
        
        n = len(X)  # 样本数
        m = len(X[0])  # 特征数
        
        # 计算 X^T * X (m x m)
        XtX = [[0.0] * m for _ in range(m)]
        for i in range(m):
            for j in range(m):
                for k in range(n):
                    XtX[i][j] += X[k][i] * X[k][j]
        
        # 计算 X^T * y (m,)
        Xty = [0.0] * m
        for i in range(m):
            for k in range(n):
                Xty[i] += X[k][i] * y[k]
        
        # 求逆 (简化版本，使用高斯-乔丹消元)
        try:
            XtX_inv = self._matrix_inverse(XtX)
        except:
            # 如果矩阵奇异，添加小的正则化项
            for i in range(m):
                XtX[i][i] += 1e-8
            
            try:
                XtX_inv = self._matrix_inverse(XtX)
            except:
                # 降级到简单平均
                return [sum(y) / len(y)] + [0.0] * (m - 1)
        
        # 计算系数: θ = X^T * X^(-1) * X^T * y
        coefficients = [0.0] * m
        for i in range(m):
            for j in range(m):
                coefficients[i] += XtX_inv[i][j] * Xty[j]
        
        return coefficients
    
    def _matrix_inverse(self, A: List[List[float]]) -> List[List[float]]:
        """
        高斯-乔丹矩阵求逆
        
        Args:
            A: n x n 矩阵
        
        Returns:
            A^(-1): n x n 矩阵
        """
        import math
        
        n = len(A)
        
        # 创建增广矩阵 [A | I]
        aug = [[A[i][j] if j < n else (1.0 if j == i + n else 0.0) 
                for j in range(2*n)] for i in range(n)]
        
        # 前向消除
        for col in range(n):
            # 找到主元
            max_row = col
            for row in range(col + 1, n):
                if abs(aug[row][col]) > abs(aug[max_row][col]):
                    max_row = row
            
            # 交换行
            aug[col], aug[max_row] = aug[max_row], aug[col]
            
            # 检查主元是否为零
            if abs(aug[col][col]) < 1e-10:
                raise ValueError("矩阵奇异，无法求逆")
            
            # 缩放主元行
            pivot = aug[col][col]
            for j in range(2*n):
                aug[col][j] /= pivot
            
            # 消去其他行的当前列
            for row in range(n):
                if row != col:
                    factor = aug[row][col]
                    for j in range(2*n):
                        aug[row][j] -= factor * aug[col][j]
        
        # 提取逆矩阵
        inv = [[aug[i][j + n] for j in range(n)] for i in range(n)]
        
        return inv
    
    def predict(self, periods: int = 30) -> List[Dict[str, Any]]:
        """
        使用回归模型进行预测
        
        Args:
            periods: 预测周期数
        
        Returns:
            预测结果列表
        """
        if not self.is_fitted or self.data is None:
            raise ValueError("模型未训练，请先调用fit()方法")
        
        n = len(self.data)
        
        # 计算残差
        values = [d['value'] for d in self.data]
        fitted = self._get_fitted_values()
        residuals = [values[i] - fitted[i] for i in range(n)]
        std_error = (sum(r**2 for r in residuals) / max(1, n - len(self.coefficients))) ** 0.5
        
        # 生成预测
        predictions = []
        
        for i in range(1, periods + 1):
            t = n - 1 + i
            
            # 构建特征
            features = [1.0]  # bias
            
            # 多项式特征
            for d in range(1, self.max_degree + 1):
                features.append(t ** d)
            
            # 趋势特征
            if self.include_trend:
                features.append(t)
                if self.max_degree >= 2:
                    features.append(t ** 2)
            
            # 季节性特征
            if self.include_seasonality:
                for k in range(1, min(4, self.period)):
                    features.append(self._sin(t, self.period, k))
                    features.append(self._cos(t, self.period, k))
            
            # 预测
            pred_value = sum(c * f for c, f in zip(self.coefficients, features))
            
            # 置信区间
            se = std_error * (1 + sum(f ** 2 for f in features[:len(self.coefficients)]) / n) ** 0.5
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
        if not self.data or not self.coefficients:
            return []
        
        n = len(self.data)
        X, _ = self._build_features(n)
        
        fitted = []
        for i in range(n):
            pred = sum(c * f for c, f in zip(self.coefficients, X[i]))
            fitted.append(pred)
        
        return fitted


# 别名
SR = SimpleRegression
Regression = SimpleRegression
