"""
数据加载模块
支持从CSV、JSON文件和命令行加载时间序列数据
"""

import csv
import json
from typing import List, Dict, Any, Optional
from pathlib import Path


class DataLoader:
    """
    时间序列数据加载器
    
    支持的数据格式:
    - CSV 文件
    - JSON 文件
    - JSON Lines 文件
    """
    
    def __init__(self):
        self.supported_formats = ['.csv', '.json', '.jsonl']
        
    def load(self, 
             file_path: str, 
             date_col: Optional[str] = None,
             value_col: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        加载数据文件
        
        Args:
            file_path: 文件路径
            date_col: 日期列名（CSV文件需要指定）
            value_col: 数值列名（CSV文件需要指定）
        
        Returns:
            时间序列数据列表
        
        Raises:
            FileNotFoundError: 文件不存在
            ValueError: 不支持的格式
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        suffix = path.suffix.lower()
        
        if suffix not in self.supported_formats:
            raise ValueError(f"不支持的文件格式: {suffix}. 支持: {', '.join(self.supported_formats)}")
        
        if suffix == '.csv':
            return self._load_csv(path, date_col, value_col)
        elif suffix == '.json':
            return self._load_json(path)
        elif suffix == '.jsonl':
            return self._load_jsonl(path)
        
        return []
    
    def _load_csv(self, 
                  path: Path,
                  date_col: Optional[str],
                  value_col: Optional[str]) -> List[Dict[str, Any]]:
        """
        加载CSV文件
        
        CSV格式要求:
        - 必须有日期列和数值列
        - 自动检测列名（识别 'date', 'time', 'value', 'y', 'close' 等常见列名）
        """
        data = []
        
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            if not rows:
                raise ValueError("CSV文件为空")
            
            # 自动检测列名
            if date_col is None:
                date_col = self._detect_date_column(rows[0].keys())
            
            if value_col is None:
                value_col = self._detect_value_column(rows[0].keys())
            
            if not date_col or not value_col:
                raise ValueError(
                    "无法自动检测日期列和数值列。\n"
                    "请使用 --date-col 和 --value-col 参数指定列名。"
                )
            
            for row in rows:
                try:
                    # 解析日期
                    date = row.get(date_col, '')
                    if not date:
                        continue
                    
                    # 解析数值
                    value_str = row.get(value_col, '0')
                    value = self._parse_value(value_str)
                    
                    data.append({
                        'date': str(date).strip(),
                        'value': value
                    })
                except (ValueError, TypeError) as e:
                    # 跳过无效行
                    continue
        
        if not data:
            raise ValueError("CSV文件中没有有效的数据行")
        
        return data
    
    def _detect_date_column(self, columns) -> Optional[str]:
        """
        自动检测日期列
        
        检查常见的列名模式
        """
        date_patterns = [
            'date', 'time', 'timestamp', 'datetime', 'day', 'month',
            'year', 'created', 'updated', 'period', 'period', 'ds'
        ]
        
        columns_lower = {col.lower() for col in columns}
        
        for pattern in date_patterns:
            if pattern in columns_lower:
                # 返回原始列名
                for col in columns:
                    if col.lower() == pattern:
                        return col
        
        return None
    
    def _detect_value_column(self, columns) -> Optional[str]:
        """
        自动检测数值列
        
        检查常见的列名模式
        """
        value_patterns = [
            'value', 'y', 'close', 'price', 'amount', 'count', 'total',
            'sales', 'revenue', 'cost', 'number', 'quantity', 'val'
        ]
        
        columns_lower = {col.lower() for col in columns}
        
        for pattern in value_patterns:
            if pattern in columns_lower:
                for col in columns:
                    if col.lower() == pattern:
                        return col
        
        return None
    
    def _parse_value(self, value_str: str) -> float:
        """
        解析数值字符串
        
        处理各种格式:
        - 普通数字: "123.45"
        - 带逗号: "1,234.56"
        - 带货币符号: "$123.45"
        - 科学计数法: "1.23e-4"
        """
        # 移除常见前缀
        value_str = value_str.strip()
        value_str = value_str.replace('$', '').replace('¥', '').replace('€', '')
        value_str = value_str.replace('£', '').replace('₹', '')
        
        # 移除逗号
        value_str = value_str.replace(',', '')
        
        # 移除百分号（转换为小数）
        if value_str.endswith('%'):
            value_str = value_str[:-1]
            return float(value_str) / 100
        
        return float(value_str)
    
    def _load_json(self, path: Path) -> List[Dict[str, Any]]:
        """
        加载JSON文件
        
        支持两种格式:
        1. 数组格式: [{"date": "2024-01-01", "value": 100}, ...]
        2. 对象格式: {"data": [...], "dates": [...], "values": [...]}
        """
        with open(path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        # 格式1: 直接是数组
        if isinstance(content, list):
            return self._normalize_json_list(content)
        
        # 格式2: 对象包含数组
        if isinstance(content, dict):
            # 尝试常见的键名
            for key in ['data', 'records', 'items', 'series']:
                if key in content and isinstance(content[key], list):
                    return self._normalize_json_list(content[key])
            
            # 尝试分离的dates和values
            if 'dates' in content and 'values' in content:
                dates = content['dates']
                values = content['values']
                
                if len(dates) == len(values):
                    return [
                        {'date': str(dates[i]), 'value': float(values[i])}
                        for i in range(len(dates))
                    ]
        
        raise ValueError("无法解析JSON文件格式")
    
    def _normalize_json_list(self, data: List[Any]) -> List[Dict[str, Any]]:
        """标准化JSON列表数据"""
        result = []
        
        for item in data:
            if isinstance(item, dict):
                # 提取日期和数值
                date = item.get('date') or item.get('time') or item.get('timestamp') or str(item.get('ds', ''))
                value = item.get('value') or item.get('y') or item.get('close') or item.get('price')
                
                if date and value is not None:
                    result.append({
                        'date': str(date),
                        'value': float(value)
                    })
            elif isinstance(item, (int, float)):
                # 纯数值数组，使用索引作为日期
                result.append({
                    'date': str(len(result) + 1),
                    'value': float(item)
                })
        
        return result
    
    def _load_jsonl(self, path: Path) -> List[Dict[str, Any]]:
        """加载JSON Lines文件"""
        result = []
        
        with open(path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    item = json.loads(line)
                    
                    if isinstance(item, dict):
                        date = item.get('date') or item.get('time') or str(line_num)
                        value = item.get('value') or item.get('y') or item.get('close')
                        
                        if value is not None:
                            result.append({
                                'date': str(date),
                                'value': float(value)
                            })
                    elif isinstance(item, (int, float)):
                        result.append({
                            'date': str(len(result) + 1),
                            'value': float(item)
                        })
                except json.JSONDecodeError:
                    continue
        
        return result
    
    def from_list(self, values: List[float], start_date: str = '1') -> List[Dict[str, Any]]:
        """
        从数值列表创建时间序列数据
        
        Args:
            values: 数值列表
            start_date: 起始日期
        
        Returns:
            时间序列数据列表
        """
        return [
            {'date': str(int(start_date) + i), 'value': float(v)}
            for i, v in enumerate(values)
        ]
    
    def from_dict(self, data: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        从字典创建时间序列数据
        
        Args:
            data: {date: value} 格式的字典
        
        Returns:
            时间序列数据列表
        """
        return [
            {'date': str(date), 'value': float(value)}
            for date, value in data.items()
        ]
