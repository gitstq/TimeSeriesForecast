"""
输出格式化模块
负责将预测结果格式化为不同的输出格式
"""

import json
from typing import List, Dict, Any, Optional
from pathlib import Path


class OutputFormatter:
    """
    预测结果格式化器
    
    支持多种输出格式:
    - 终端表格显示
    - JSON
    - CSV
    - Markdown表格
    """
    
    def __init__(self):
        self.precision = 2
        
    def format_predictions(self, 
                          predictions: List[Dict[str, Any]],
                          format: str = 'table') -> str:
        """
        格式化预测结果
        
        Args:
            predictions: 预测结果列表
            format: 输出格式 ('table', 'json', 'csv', 'markdown')
        
        Returns:
            格式化后的字符串
        """
        if format == 'json':
            return self._format_json(predictions)
        elif format == 'csv':
            return self._format_csv(predictions)
        elif format == 'markdown':
            return self._format_markdown(predictions)
        else:
            return self._format_table(predictions)
    
    def _format_table(self, predictions: List[Dict[str, Any]]) -> str:
        """格式化为终端表格"""
        if not predictions:
            return "无预测结果"
        
        lines = []
        
        # 表头
        header = f"{'周期':^8} | {'预测值':^12} | {'下限':^12} | {'上限':^12}"
        separator = f"{'-' * 8}-+-{'-' * 12}-+-{'-' * 12}-+-{'-' * 12}"
        
        lines.append(header)
        lines.append(separator)
        
        # 数据行
        for pred in predictions[:20]:  # 最多显示20行
            period = f"{pred.get('period', 0):^8}"
            value = f"{pred.get('value', 0):>12.{self.precision}f}"
            lower = f"{pred.get('lower', 0):>12.{self.precision}f}"
            upper = f"{pred.get('upper', 0):>12.{self.precision}f}"
            
            lines.append(f"{period} | {value} | {lower} | {upper}")
        
        if len(predictions) > 20:
            lines.append(f"\n... (共 {len(predictions)} 条预测)")
        
        return '\n'.join(lines)
    
    def _format_json(self, predictions: List[Dict[str, Any]]) -> str:
        """格式化为JSON"""
        # 转换numpy类型（如果有）为原生Python类型
        data = []
        for pred in predictions:
            data.append({
                'period': int(pred.get('period', 0)),
                'value': round(float(pred.get('value', 0)), self.precision),
                'lower_bound': round(float(pred.get('lower', 0)), self.precision),
                'upper_bound': round(float(pred.get('upper', 0)), self.precision)
            })
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def _format_csv(self, predictions: List[Dict[str, Any]]) -> str:
        """格式化为CSV"""
        lines = ["period,value,lower,upper"]
        
        for pred in predictions:
            period = pred.get('period', 0)
            value = round(pred.get('value', 0), self.precision)
            lower = round(pred.get('lower', 0), self.precision)
            upper = round(pred.get('upper', 0), self.precision)
            
            lines.append(f"{period},{value},{lower},{upper}")
        
        return '\n'.join(lines)
    
    def _format_markdown(self, predictions: List[Dict[str, Any]]) -> str:
        """格式化为Markdown表格"""
        lines = []
        
        # 表头
        lines.append("| 周期 | 预测值 | 95% CI 下限 | 95% CI 上限 |")
        lines.append("|------|--------|------------|------------|")
        
        # 数据行
        for pred in predictions[:30]:  # 最多显示30行
            period = pred.get('period', 0)
            value = round(pred.get('value', 0), self.precision)
            lower = round(pred.get('lower', 0), self.precision)
            upper = round(pred.get('upper', 0), self.precision)
            
            lines.append(f"| {period} | {value} | {lower} | {upper} |")
        
        if len(predictions) > 30:
            lines.append(f"\n*... 共 {len(predictions)} 条预测结果*")
        
        return '\n'.join(lines)
    
    def format_metrics(self, metrics: Dict[str, float]) -> str:
        """
        格式化评估指标
        
        Args:
            metrics: 评估指标字典
        
        Returns:
            格式化后的字符串
        """
        lines = ["📊 模型评估指标", ""]
        
        metric_names = {
            'RMSE': '均方根误差 (RMSE)',
            'MAE': '平均绝对误差 (MAE)',
            'MAPE': '平均绝对百分比误差 (MAPE)',
            'R2': '决定系数 (R²)'
        }
        
        for key, value in metrics.items():
            name = metric_names.get(key, key)
            lines.append(f"  • **{name}**: {value:.{self.precision}f}")
        
        return '\n'.join(lines)
    
    def format_summary(self, 
                      data: List[Dict[str, Any]],
                      predictions: List[Dict[str, Any]],
                      metrics: Dict[str, float]) -> str:
        """
        格式化完整的预测摘要
        
        Args:
            data: 原始数据
            predictions: 预测结果
            metrics: 评估指标
        
        Returns:
            摘要字符串
        """
        lines = []
        
        # 标题
        lines.append("=" * 60)
        lines.append("📈 TimeSeriesForecast 预测报告")
        lines.append("=" * 60)
        
        # 数据概览
        lines.append("\n📊 数据概览:")
        lines.append(f"  • 历史数据点: {len(data)}")
        lines.append(f"  • 预测周期数: {len(predictions)}")
        
        if data:
            values = [d['value'] for d in data]
            lines.append(f"  • 历史均值: {sum(values)/len(values):.{self.precision}f}")
            lines.append(f"  • 历史最小值: {min(values):.{self.precision}f}")
            lines.append(f"  • 历史最大值: {max(values):.{self.precision}f}")
        
        # 预测概览
        if predictions:
            pred_values = [p['value'] for p in predictions]
            lines.append(f"\n🔮 预测概览:")
            lines.append(f"  • 预测均值: {sum(pred_values)/len(pred_values):.{self.precision}f}")
            lines.append(f"  • 预测最小值: {min(pred_values):.{self.precision}f}")
            lines.append(f"  • 预测最大值: {max(pred_values):.{self.precision}f}")
        
        # 模型指标
        if metrics:
            lines.append("\n📉 模型评估指标:")
            for key, value in metrics.items():
                lines.append(f"  • {key}: {value:.{self.precision}f}")
        
        lines.append("\n" + "=" * 60)
        
        return '\n'.join(lines)
    
    def save_predictions(self,
                        predictions: List[Dict[str, Any]],
                        output_path: str,
                        format: Optional[str] = None):
        """
        保存预测结果到文件
        
        Args:
            predictions: 预测结果
            output_path: 输出文件路径
            format: 输出格式（自动从文件扩展名推断）
        """
        path = Path(output_path)
        
        if format is None:
            format = path.suffix.lower().lstrip('.')
        
        if format == 'json':
            content = self._format_json(predictions)
        elif format == 'csv':
            content = self._format_csv(predictions)
        elif format == 'md' or format == 'markdown':
            content = self._format_markdown(predictions)
        else:
            # 默认使用JSON
            content = self._format_json(predictions)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def format_comparison(self, results: List[Dict[str, Any]]) -> str:
        """
        格式化模型比较结果
        
        Args:
            results: 模型比较结果列表
        
        Returns:
            格式化后的字符串
        """
        if not results:
            return "无比较结果"
        
        lines = []
        
        # 表头
        header = f"{'模型':^12} | {'RMSE':^12} | {'MAE':^12} | {'MAPE':^12} |"
        separator = f"{'-' * 12}-+-{'-' * 12}-+-{'-' * 12}-+-{'-' * 12}"
        
        lines.append(header)
        lines.append(separator)
        
        # 按RMSE排序
        sorted_results = sorted(results, key=lambda x: x.get('metrics', {}).get('RMSE', float('inf')))
        
        for result in sorted_results:
            model_name = f"{result.get('name', 'unknown'):^12}"
            rmse = f"{result.get('metrics', {}).get('RMSE', 0):>12.{self.precision}f}"
            mae = f"{result.get('metrics', {}).get('MAE', 0):>12.{self.precision}f}"
            mape = f"{result.get('metrics', {}).get('MAPE', 0):>12.{self.precision}f}"
            
            lines.append(f"{model_name} | {rmse} | {mae} | {mape} |")
        
        return '\n'.join(lines)
