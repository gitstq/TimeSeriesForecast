# 📖 TimeSeriesForecast 使用指南

## 📚 目录

- [🎯 项目介绍](#🎯-项目介绍)
- [📦 安装](#📦-安装)
- [🚀 快速开始](#🚀-快速开始)
- [💡 详细用法](#💡-详细用法)
- [📊 支持的模型](#📊-支持的模型)
- [🎨 数据格式](#🎨-数据格式)
- [🔧 高级配置](#🔧-高级配置)
- [📝 示例](#📝-示例)
- [❓ 常见问题](#❓-常见问题)

---

## 🎯 项目介绍

**TimeSeriesForecast** 是一款专为开发者、数据分析师和业务人员设计的轻量级时间序列预测CLI工具。

### ✨ 核心特点

- 🔌 **零依赖** - 纯Python标准库，无需安装任何外部包
- ⚡ **一键预测** - 简单命令完成数据加载、建模、预测全流程
- 📊 **多模型支持** - 集成5种常用预测模型
- 🎨 **可视化输出** - ASCII艺术图表 + 可选Matplotlib高质量图表
- 🔧 **灵活配置** - 支持自定义预测周期、置信区间、模型参数
- 📦 **开箱即用** - pip安装即可，无需复杂配置

---

## 📦 安装

### 环境要求

- Python 3.8 或更高版本
- 无需安装任何外部依赖（零依赖设计）

### 安装方式

#### 方式1: pip安装（推荐）

```bash
pip install TimeSeriesForecast
```

#### 方式2: 从源码安装

```bash
git clone https://github.com/gitstq/TimeSeriesForecast.git
cd TimeSeriesForecast
pip install -e .
```

#### 方式3: 直接使用（无需安装）

```bash
python forecast.py run data.csv --model sma --period 30
```

---

## 🚀 快速开始

### 1. 准备数据

创建CSV文件，格式如下：

```csv
date,value
2024-01-01,100
2024-01-02,120
2024-01-03,115
2024-01-04,130
...
```

### 2. 运行预测

```bash
# 使用简单移动平均模型预测未来30天
forecast run data.csv --model sma --period 30

# 使用指数平滑模型
forecast run data.csv --model es --alpha 0.3 --period 30

# 比较多个模型
forecast compare data.csv --models sma,es,lt --period 30

# 生成预测图表
forecast plot data.csv --output forecast.png --period 60
```

### 3. 查看结果

程序会输出：
- 📊 预测趋势ASCII图表
- 📈 预测值表格（包含置信区间）
- 📉 模型评估指标（RMSE、MAE、MAPE）

---

## 💡 详细用法

### 基本命令

```bash
# 运行预测
forecast run <file> [OPTIONS]

# 比较多个模型
forecast compare <file> [OPTIONS]

# 生成图表
forecast plot <file> [OPTIONS]

# 查看帮助
forecast --help
forecast info
```

### 主要选项

| 选项 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--model` | `-m` | 预测模型 | sma |
| `--period` | `-p` | 预测周期数 | 30 |
| `--window` | `-w` | 移动平均窗口大小 | 7 |
| `--alpha` | `-a` | 指数平滑alpha值 | 0.3 |
| `--no-plot` | - | 不显示图表 | False |
| `--output` | `-o` | 保存结果到文件 | - |

---

## 📊 支持的模型

### 1. 简单移动平均 (SMA) ⭐推荐

```
forecast run data.csv --model sma --window 7 --period 30
```

**适用场景**：短期数据平滑、噪声消除
**参数**：
- `--window`：窗口大小，越大越平滑

### 2. 加权移动平均 (WMA)

```
forecast run data.csv --model wma --window 7 --period 30
```

**适用场景**：趋势跟随、近期数据更重要
**参数**：
- `--window`：窗口大小

### 3. 指数平滑 (ES)

```
forecast run data.csv --model es --alpha 0.3 --period 30
```

**适用场景**：中期预测、考虑历史权重
**参数**：
- `--alpha`：平滑系数 (0-1)，越大越重视近期数据

### 4. 线性趋势 (LT)

```
forecast run data.csv --model lt --period 30
```

**适用场景**：线性增长/下降数据
**特点**：自动拟合线性趋势

### 5. 简单回归 (SR)

```
forecast run data.csv --model sr --max-degree 2 --period 30
```

**适用场景**：多项式趋势、复杂关系
**参数**：
- `--max-degree`：多项式最高次数

### 模型比较

```bash
# 自动比较多个模型并排名
forecast compare data.csv --models sma,es,lt,sr --top-k 3
```

输出示例：

```
📊 模型排名 (按RMSE):
   1. es - RMSE: 5.2342
   2. lt - RMSE: 6.1234
   3. sma - RMSE: 7.5678
```

---

## 🎨 数据格式

### 支持的格式

#### 1. CSV文件（推荐）

```csv
date,value
2024-01-01,100
2024-01-02,120
2024-01-03,115
```

自动识别列名：
- 日期列：`date`, `time`, `timestamp`, `datetime`
- 数值列：`value`, `y`, `close`, `price`, `amount`

#### 2. JSON文件

```json
[
  {"date": "2024-01-01", "value": 100},
  {"date": "2024-01-02", "value": 120}
]
```

或

```json
{
  "data": [
    {"date": "2024-01-01", "value": 100}
  ]
}
```

#### 3. JSON Lines文件

```jsonl
{"date": "2024-01-01", "value": 100}
{"date": "2024-01-02", "value": 120}
```

### 指定列名

如果自动识别失败，可手动指定：

```bash
forecast run data.csv --date-col my_date --value-col my_value
```

---

## 🔧 高级配置

### 数据预处理

#### 缺失值填充

```bash
# 线性插值（默认）
forecast run data.csv --fill-method linear

# 前向填充
forecast run data.csv --fill-method forward

# 后向填充
forecast run data.csv --fill-method backward

# 均值填充
forecast run data.csv --fill-method mean

# 填充为0
forecast run data.csv --fill-method zero
```

#### 异常值处理

自动处理3倍IQR以外的异常值

### 输出格式

```bash
# 保存为JSON
forecast run data.csv --output result.json --format json

# 保存为CSV
forecast run data.csv --output result.csv --format csv

# 保存为Markdown
forecast run data.csv --output result.md --format markdown
```

### 图表生成

#### ASCII图表（默认，无需额外依赖）

```bash
forecast run data.csv --no-plot
```

#### Matplotlib图表（需要安装matplotlib）

```bash
# 先安装matplotlib
pip install matplotlib

# 生成PNG图表
forecast plot data.csv --output forecast.png --period 60

# 自定义尺寸
forecast plot data.csv --output forecast.png --width 1200 --height 800
```

---

## 📝 示例

### 示例1：销售数据预测

```bash
# 准备数据 sales.csv
# date,amount
# 2024-01-01,5000
# 2024-01-02,5500
# ...

# 运行预测
forecast run sales.csv --model es --alpha 0.3 --period 30 --output sales_forecast.json
```

### 示例2：股票价格预测

```bash
# 使用线性趋势模型
forecast run stock.csv --model lt --period 90

# 比较多个模型
forecast compare stock.csv --models sma,es,lt --period 90 --top-k 2
```

### 示例3：网站访问量预测

```bash
# 使用移动平均模型
forecast run traffic.csv --model sma --window 7 --period 30

# 生成趋势图
forecast plot traffic.csv --output traffic_forecast.png --period 30
```

### 示例4：API调用量预测

```bash
# 使用指数平滑
forecast run api_calls.csv --model es --alpha 0.5 --period 60 --output api_forecast.json
```

---

## ❓ 常见问题

### Q1: 安装失败？

**A**: 确保Python版本>=3.8，并使用pip最新版本：

```bash
pip install --upgrade pip
pip install TimeSeriesForecast
```

### Q2: 数据加载失败？

**A**: 检查数据格式：
- 确保CSV/JSON文件编码为UTF-8
- 确保日期列和数值列存在且正确
- 使用`--date-col`和`--value-col`指定列名

### Q3: 预测结果不准确？

**A**: 尝试以下方法：
1. 增加历史数据量
2. 选择合适的模型（使用`compare`命令比较）
3. 调整模型参数（如alpha、window）
4. 检查数据是否有异常值

### Q4: 如何处理季节性数据？

**A**: 对于季节性数据，建议：
1. 使用指数平滑模型（ES）
2. 分解季节性成分
3. 考虑使用Prophet等专用工具

### Q5: 命令行提示"command not found"？

**A**: 确保安装成功：
```bash
pip show TimeSeriesForecast
```

如果未找到，尝试：
```bash
python -m forecast run data.csv --model sma --period 30
```

### Q6: 如何获取更详细的日志？

**A**: 使用调试模式：
```bash
forecast --debug run data.csv --model sma --period 30
```

---

## 📞 技术支持

- 📋 Issue: https://github.com/gitstq/TimeSeriesForecast/issues
- 📖 文档: https://github.com/gitstq/TimeSeriesForecast#readme
- 💬 讨论: https://github.com/gitstq/TimeSeriesForecast/discussions

---

<p align="center">
  ⭐ 如果这个项目对您有帮助，请给我们一个星标！
</p>
