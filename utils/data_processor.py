"""
数据处理模块
包含数据预处理、清洗、转换等功能
"""

from typing import List, Dict, Any, Optional
import math


class DataProcessor:
    """
    时间序列数据处理器
    
    功能:
    - 缺失值处理
    - 异常值检测
    - 数据归一化
    - 时间频率推断
    """
    
    def __init__(self):
        self.stats = {}
        
    def process(self, 
                data: List[Dict[str, Any]], 
                fill_method: str = 'linear') -> List[Dict[str, Any]]:
        """
        处理时间序列数据
        
        Args:
            data: 原始数据
            fill_method: 缺失值填充方法 ('linear', 'forward', 'backward', 'mean', 'zero')
        
        Returns:
            处理后的数据
        """
        if not data:
            return data
        
        # 1. 缺失值处理
        data = self._handle_missing_values(data, fill_method)
        
        # 2. 异常值处理
        data = self._handle_outliers(data)
        
        # 3. 计算统计信息
        self._compute_statistics(data)
        
        return data
    
    def _handle_missing_values(self,
                               data: List[Dict[str, Any]],
                               method: str = 'linear') -> List[Dict[str, Any]]:
        """
        处理缺失值
        
        Args:
            data: 时间序列数据
            method: 填充方法
        
        Returns:
            填充后的数据
        """
        # 统计缺失值
        missing_count = sum(1 for d in data if d.get('value') is None or math.isnan(d.get('value', 0)))
        
        if missing_count == 0:
            return data
        
        # 提取有效值
        values = [d['value'] for d in data]
        valid_values = [v for v in values if v is not None and not math.isnan(v)]
        
        if not valid_values:
            # 全是缺失值，无法填充
            return data
        
        mean_value = sum(valid_values) / len(valid_values)
        
        # 根据方法填充
        if method == 'zero':
            # 填充为0
            filled = [0 if (v is None or math.isnan(v)) else v for v in values]
        elif method == 'mean':
            # 填充为均值
            filled = [mean_value if (v is None or math.isnan(v)) else v for v in values]
        elif method == 'forward':
            # 前向填充
            filled = self._forward_fill(values)
        elif method == 'backward':
            # 后向填充
            filled = self._backward_fill(values)
        elif method == 'linear':
            # 线性插值
            filled = self._linear_interpolate(values)
        else:
            filled = values
        
        # 更新数据
        for i, d in enumerate(data):
            d['value'] = filled[i]
        
        return data
    
    def _forward_fill(self, values: List[float]) -> List[float]:
        """前向填充"""
        result = values.copy()
        last_valid = None
        
        for i, v in enumerate(result):
            if v is None or math.isnan(v):
                if last_valid is not None:
                    result[i] = last_valid
            else:
                last_valid = v
        
        return result
    
    def _backward_fill(self, values: List[float]) -> List[float]:
        """后向填充"""
        result = values.copy()
        next_valid = None
        
        for i in range(len(result) - 1, -1, -1):
            v = result[i]
            if v is None or math.isnan(v):
                if next_valid is not None:
                    result[i] = next_valid
            else:
                next_valid = v
        
        return result
    
    def _linear_interpolate(self, values: List[float]) -> List[float]:
        """线性插值"""
        result = values.copy()
        n = len(values)
        
        # 找到第一个和最后一个有效值的位置
        first_valid_idx = None
        last_valid_idx = None
        
        for i, v in enumerate(values):
            if v is not None and not math.isnan(v):
                if first_valid_idx is None:
                    first_valid_idx = i
                last_valid_idx = i
        
        if first_valid_idx is None:
            return result
        
        # 对于开头的缺失值，使用第一个有效值
        for i in range(first_valid_idx):
            result[i] = values[first_valid_idx]
        
        # 对于结尾的缺失值，使用最后一个有效值
        for i in range(last_valid_idx + 1, n):
            result[i] = values[last_valid_idx]
        
        # 线性插值中间部分
        i = first_valid_idx
        while i <= last_valid_idx:
            if result[i] is None or math.isnan(result[i]):
                # 找到下一个有效值
                j = i + 1
                while j <= last_valid_idx and (result[j] is None or math.isnan(result[j])):
                    j += 1
                
                if j <= last_valid_idx:
                    # 在 i 和 j 之间插值
                    start_val = values[i - 1] if i > 0 else values[i]
                    end_val = values[j]
                    step = (end_val - start_val) / (j - i + 1)
                    
                    for k in range(i, j):
                        result[k] = start_val + step * (k - i + 1)
                
                i = j
            else:
                i += 1
        
        return result
    
    def _handle_outliers(self, 
                         data: List[Dict[str, Any]], 
                         method: str = 'iqr',
                         threshold: float = 3.0) -> List[Dict[str, Any]]:
        """
        异常值检测和处理
        
        Args:
            data: 时间序列数据
            method: 检测方法 ('iqr', 'zscore')
            threshold: 阈值
        
        Returns:
            处理后的数据
        """
        if len(data) < 4:
            return data
        
        values = [d['value'] for d in data]
        
        if method == 'zscore':
            # Z-score方法
            mean = sum(values) / len(values)
            variance = sum((v - mean) ** 2 for v in values) / len(values)
            std = math.sqrt(variance) if variance > 0 else 1
            
            for i, d in enumerate(data):
                z_score = abs((values[i] - mean) / std)
                if z_score > threshold:
                    # 使用中位数替换
                    sorted_values = sorted(values)
                    median = sorted_values[len(sorted_values) // 2]
                    d['value'] = median
        else:
            # IQR方法
            sorted_values = sorted(values)
            n = len(sorted_values)
            
            q1 = sorted_values[n // 4]
            q3 = sorted_values[3 * n // 4]
            iqr = q3 - q1
            
            lower_bound = q1 - threshold * iqr
            upper_bound = q3 + threshold * iqr
            
            for d in data:
                if d['value'] < lower_bound or d['value'] > upper_bound:
                    # 使用边界值替换
                    d['value'] = max(lower_bound, min(upper_bound, d['value']))
        
        return data
    
    def _compute_statistics(self, data: List[Dict[str, Any]]):
        """计算数据统计信息"""
        if not data:
            return
        
        values = [d['value'] for d in data]
        n = len(values)
        
        # 均值
        mean = sum(values) / n
        
        # 方差和标准差
        variance = sum((v - mean) ** 2 for v in values) / n
        std = math.sqrt(variance)
        
        # 最小值、最大值
        min_val = min(values)
        max_val = max(values)
        
        # 中位数
        sorted_values = sorted(values)
        median = sorted_values[n // 2]
        
        # 变异系数
        cv = (std / mean * 100) if mean != 0 else 0
        
        self.stats = {
            'count': n,
            'mean': mean,
            'std': std,
            'min': min_val,
            'max': max_val,
            'median': median,
            'cv': cv,  # 变异系数 (%)
            'variance': variance
        }
    
    def get_statistics(self) -> Dict[str, float]:
        """获取统计信息"""
        return self.stats.copy()
    
    def normalize(self, 
                 data: List[Dict[str, Any]], 
                 method: str = 'minmax') -> List[Dict[str, Any]]:
        """
        数据归一化
        
        Args:
            data: 时间序列数据
            method: 归一化方法 ('minmax', 'zscore')
        
        Returns:
            归一化后的数据
        """
        if not data:
            return data
        
        values = [d['value'] for d in data]
        result = []
        
        if method == 'minmax':
            min_val = min(values)
            max_val = max(values)
            range_val = max_val - min_val
            
            if range_val == 0:
                range_val = 1
            
            for d in data:
                normalized = (d['value'] - min_val) / range_val
                result.append({
                    'date': d['date'],
                    'value': normalized
                })
        elif method == 'zscore':
            mean = sum(values) / len(values)
            variance = sum((v - mean) ** 2 for v in values) / len(values)
            std = math.sqrt(variance) if variance > 0 else 1
            
            for d in data:
                normalized = (d['value'] - mean) / std
                result.append({
                    'date': d['date'],
                    'value': normalized
                })
        else:
            return data
        
        return result
    
    def detect_frequency(self, data: List[Dict[str, Any]]) -> Optional[str]:
        """
        推断时间频率
        
        Returns:
            频率描述 ('daily', 'weekly', 'monthly', 'yearly')
        """
        if len(data) < 2:
            return None
        
        # 简化实现：检查数据点数量和跨度
        n = len(data)
        
        # 假设数据是连续的
        if n <= 31:
            return 'daily'
        elif n <= 365:
            return 'weekly'
        elif n <= 3650:
            return 'monthly'
        else:
            return 'yearly'
