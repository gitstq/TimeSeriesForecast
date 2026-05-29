"""
ASCII艺术图表生成器
在终端中显示时间序列趋势图
"""

from typing import List, Dict, Any, Optional


class AsciiChart:
    """
    ASCII艺术图表生成器
    
    使用纯ASCII字符在终端绘制时间序列趋势图
    """
    
    def __init__(self, 
                 width: int = 60,
                 height: int = 15):
        """
        初始化ASCII图表生成器
        
        Args:
            width: 图表宽度（字符数）
            height: 图表高度（字符数）
        """
        self.width = width
        self.height = height
        
    def render(self, 
               data: List[Dict[str, Any]], 
               predictions: Optional[List[Dict[str, Any]]] = None,
               show_confidence: bool = True) -> str:
        """
        渲染ASCII趋势图
        
        Args:
            data: 历史数据
            predictions: 预测数据
            show_confidence: 是否显示置信区间
        
        Returns:
            ASCII图表字符串
        """
        if not data:
            return "无数据可显示"
        
        # 合并历史数据和预测数据
        all_values = [d['value'] for d in data]
        if predictions:
            all_values.extend([p['value'] for p in predictions])
        
        if not all_values:
            return "无数据可显示"
        
        # 计算数值范围
        min_val = min(all_values)
        max_val = max(all_values)
        
        # 如果所有值相同，添加一些偏移
        if min_val == max_val:
            min_val -= 1
            max_val += 1
        
        # 处理置信区间
        if show_confidence and predictions:
            lower_vals = [p['lower'] for p in predictions]
            upper_vals = [p['upper'] for p in predictions]
            min_val = min(min_val, min(lower_vals))
            max_val = max(max_val, max(upper_vals))
        
        # 构建图表
        lines = []
        
        # 标题
        lines.append("📈 时间序列趋势图")
        lines.append("=" * self.width)
        
        # 创建图表网格
        chart = self._create_chart(
            data, 
            predictions, 
            min_val, 
            max_val, 
            show_confidence
        )
        
        lines.extend(chart)
        
        # 添加图例
        lines.append("")
        legend = self._create_legend(show_confidence and predictions is not None)
        lines.append(legend)
        
        return '\n'.join(lines)
    
    def _create_chart(self,
                     data: List[Dict[str, Any]],
                     predictions: Optional[List[Dict[str, Any]]],
                     min_val: float,
                     max_val: float,
                     show_confidence: bool) -> List[str]:
        """创建图表内容"""
        # 初始化网格
        grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # 绘制置信区间（背景）
        if show_confidence and predictions:
            self._draw_confidence_interval(grid, predictions, min_val, max_val)
        
        # 绘制历史数据线
        self._draw_line(grid, data, min_val, max_val, '●')
        
        # 绘制预测数据线
        if predictions:
            # 计算历史数据点的数量
            offset = len(data)
            
            # 为预测数据创建简化的时间索引
            pred_data = [
                {'value': p['value']}
                for p in predictions
            ]
            
            self._draw_line(grid, pred_data, min_val, max_val, '◆', offset)
        
        # 转换为字符串
        lines = []
        value_range = max_val - min_val
        
        for row in range(self.height):
            # 计算Y轴标签
            y_val = max_val - (row / (self.height - 1)) * value_range
            
            # Y轴刻度线
            if row == 0:
                label = f"{max_val:>8.1f} ┤"
            elif row == self.height - 1:
                label = f"{min_val:>8.1f} ┤"
            elif row == self.height // 2:
                mid_val = (max_val + min_val) / 2
                label = f"{mid_val:>8.1f} ┤"
            else:
                label = " " * 9 + "├"
            
            # 图表行
            chart_row = ''.join(grid[row])
            lines.append(label + chart_row)
        
        # X轴
        x_axis = " " * 9 + "└" + "─" * self.width
        lines.append(x_axis)
        
        # X轴标签
        x_labels = self._create_x_labels(len(data), len(predictions) if predictions else 0)
        lines.append(" " * 9 + x_labels)
        
        return lines
    
    def _draw_line(self, 
                   grid: List[List[str]], 
                   data: List[Dict[str, Any]], 
                   min_val: float,
                   max_val: float,
                   symbol: str = '●',
                   offset: int = 0):
        """绘制数据线"""
        if not data:
            return
        
        n = len(data)
        values = [d['value'] for d in data]
        
        # 计算每个数据点占用的列数
        step = max(1, (n - 1) / self.width) if n > 1 else 1
        
        # 绘制数据点
        for i, value in enumerate(values):
            # 计算列位置
            if n > 1:
                col = int(offset + (i / (n - 1)) * (self.width - 1))
            else:
                col = offset
            
            col = max(0, min(col, self.width - 1))
            
            # 计算行位置
            row = self._value_to_row(value, min_val, max_val)
            
            if 0 <= row < self.height:
                grid[row][col] = symbol
    
    def _draw_confidence_interval(self,
                                  grid: List[List[str]],
                                  predictions: List[Dict[str, Any]],
                                  min_val: float,
                                  max_val: float):
        """绘制置信区间"""
        n = len(predictions)
        
        if n < 2:
            return
        
        # 简化实现：只绘制上下边界
        step = max(1, (n - 1) / self.width)
        
        for i in range(n):
            pred = predictions[i]
            
            # 计算列位置
            col = int((i / (n - 1)) * (self.width - 1))
            col = max(0, min(col, self.width - 1))
            
            # 上边界
            upper_row = self._value_to_row(pred['upper'], min_val, max_val)
            if 0 <= upper_row < self.height:
                if grid[upper_row][col] == ' ':
                    grid[upper_row][col] = '╮'
            
            # 下边界
            lower_row = self._value_to_row(pred['lower'], min_val, max_val)
            if 0 <= lower_row < self.height:
                if grid[lower_row][col] == ' ':
                    grid[lower_row][col] = '╯'
            
            # 填充中间区域
            for row in range(upper_row + 1, lower_row):
                if 0 <= row < self.height:
                    if grid[row][col] == ' ':
                        grid[row][col] = '─'
    
    def _value_to_row(self, value: float, min_val: float, max_val: float) -> int:
        """将数值转换为行索引"""
        if max_val == min_val:
            return self.height // 2
        
        # 反转：因为Y轴上方是大值
        normalized = (value - min_val) / (max_val - min_val)
        row = int((1 - normalized) * (self.height - 1))
        
        return max(0, min(row, self.height - 1))
    
    def _create_x_labels(self, history_len: int, pred_len: int) -> str:
        """创建X轴标签"""
        total_len = history_len + pred_len
        
        if total_len <= 0:
            return ""
        
        # 简化的X轴标签
        if total_len <= 10:
            labels = [str(i) for i in range(1, total_len + 1)]
        else:
            # 每隔几个点显示一个标签
            step = max(1, total_len // 10)
            labels = []
            for i in range(0, total_len, step):
                labels.append(str(i + 1))
        
        # 调整标签长度以适应宽度
        label_str = ''.join(labels)[:self.width]
        
        return label_str
    
    def _create_legend(self, has_confidence: bool) -> str:
        """创建图例"""
        legend_items = ["● 历史数据"]
        
        if has_confidence:
            legend_items.append("◆ 预测值")
            legend_items.append("╮╯ 置信区间")
        
        # 居中对齐
        legend = "  ".join(legend_items)
        padding = (self.width - len(legend)) // 2
        legend = " " * max(0, padding) + legend
        
        return legend
    
    def render_comparison(self, results: List[Dict[str, Any]]) -> str:
        """
        渲染多模型比较图表
        
        Args:
            results: 模型比较结果
        
        Returns:
            ASCII图表
        """
        lines = []
        
        lines.append("📊 模型预测对比图")
        lines.append("=" * self.width)
        
        # 简化的柱状图比较
        metrics = ['RMSE', 'MAE']
        
        for metric in metrics:
            lines.append(f"\n{metric}:")
            
            # 找到最大值用于归一化
            max_val = max(
                (r.get('metrics', {}).get(metric, 0) for r in results),
                default=1
            )
            
            if max_val == 0:
                max_val = 1
            
            for result in results:
                name = result.get('name', 'unknown')[:8].ljust(8)
                value = result.get('metrics', {}).get(metric, 0)
                
                # 计算条形长度
                bar_len = int((value / max_val) * (self.width - 15))
                bar = '█' * bar_len
                
                lines.append(f"  {name} │{bar} {value:.2f}")
        
        return '\n'.join(lines)
