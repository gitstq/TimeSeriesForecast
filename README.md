# TimeSeriesForecast

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Dependencies-Zero-brightgreen.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/License-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/github/stars/gitstq/TimeSeriesForecast?style=social" alt="Stars">
</p>

<p align="center">
  🚀 轻量级时间序列预测CLI工具 | 零依赖、开箱即用、多模型支持
</p>

<p align="center">
  <a href="https://github.com/gitstq/TimeSeriesForecast">English</a> • 
  <a href="https://github.com/gitstq/TimeSeriesForecast/blob/main/docs/README_zh-CN.md">简体中文</a> • 
  <a href="https://github.com/gitstq/TimeSeriesForecast/blob/main/docs/README_zh-TW.md">繁體中文</a> •
  <a href="https://github.com/gitstq/TimeSeriesForecast/blob/main/docs/README_ja.md">日本語</a>
</p>

---

## 🎯 项目介绍

**TimeSeriesForecast** 是一款专为开发者、数据分析师和业务人员设计的**轻量级时间序列预测CLI工具**。它具有以下核心特点：

### ✨ 核心亮点

- 🔌 **零依赖设计** - 纯Python标准库实现，无需安装任何外部依赖
- ⚡ **一键预测** - 简单命令即可完成数据加载、建模、预测全流程
- 📊 **多模型支持** - 集成简单移动平均、指数平滑、线性趋势等多种预测方法
- 🎨 **可视化输出** - 自动生成ASCII艺术图表和趋势预览
- 🔧 **灵活配置** - 支持自定义预测周期、置信区间、模型参数
- 📦 **开箱即用** - pip安装即可使用，无需复杂配置

### 🎯 解决的用户痛点

1. **复杂配置门槛高** - 传统时间序列工具（如Prophet、ARIMA）需要复杂的参数配置
2. **依赖安装繁琐** - 大多数预测工具依赖众多Python库，安装困难
3. **缺乏快速预览** - 无法快速预览数据趋势和预测结果
4. **输出格式单一** - 无法满足不同场景的输出需求

## 📦 快速开始

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

### 基本用法

#### 1. 准备数据文件

创建CSV文件，格式如下：

```csv
date,value
2024-01-01,100
2024-01-02,120
2024-01-03,115
...
```

#### 2. 运行预测

```bash
# 使用简单移动平均模型预测
forecast run data.csv --model sma --period 30

# 使用指数平滑模型
forecast run data.csv --model es --alpha 0.3 --period 30

# 查看模型信息
forecast info
```

#### 3. 比较多个模型

```bash
forecast compare data.csv --models sma,es,lt --period 30
```

#### 4. 生成图表

```bash
forecast plot data.csv --output forecast.png --period 60
```

## 🎓 详细使用指南

### 支持的预测模型

| 模型 | 参数 | 适用场景 | 特点 |
|------|------|---------|------|
| **SMA** | `--window` | 短期平滑 | 快速、对噪声敏感 |
| **WMA** | `--window` | 趋势跟随 | 可调权重 |
| **ES** | `--alpha` | 中期预测 | 考虑历史权重 |
| **LT** | - | 线性增长 | 简单直观 |
| **SR** | `--max-degree` | 关系预测 | 可处理多特征 |

### 完整命令选项

```bash
forecast run [OPTIONS] FILE

选项:
  --model, -m [sma|wma|es|lt|sr]  预测模型 (默认: sma)
  --period, -p INTEGER             预测周期数 (默认: 30)
  --window, -w INTEGER              移动平均窗口大小 (默认: 7)
  --alpha, -a FLOAT                指数平滑alpha值 (默认: 0.3)
  --date-col TEXT                   日期列名
  --value-col TEXT                  数值列名
  --no-plot                         不显示图表
  --output, -o FILE                保存结果到文件
```

### 数据格式支持

- ✅ CSV 文件（自动检测列名）
- ✅ JSON 文件
- ✅ JSON Lines 文件
- ✅ 命令行直接输入数据点

## 🏗️ 架构设计

### 技术选型

- **编程语言**: Python 3.8+
- **依赖库**: 零外部依赖，仅使用Python标准库
- **CLI框架**: 纯argparse实现
- **图表渲染**: ASCII艺术 + Matplotlib（可选）

### 项目结构

```
TimeSeriesForecast/
├── forecast.py              # 主入口，CLI解析
├── models/
│   ├── base.py             # 基类定义
│   ├── moving_average.py   # 移动平均模型
│   ├── exponential_smoothing.py  # 指数平滑模型
│   ├── linear_trend.py    # 线性趋势模型
│   └── simple_regression.py  # 简单回归模型
├── utils/
│   ├── data_loader.py     # 数据加载模块
│   ├── data_processor.py  # 数据预处理
│   └── output_formatter.py # 输出格式化
├── visualization/
│   ├── ascii_chart.py     # ASCII图表生成
│   └── chart_generator.py # Matplotlib图表生成
└── tests/
    └── test_models.py      # 单元测试
```

## 📊 性能基准

| 数据规模 | 预测模型 | 耗时 | 内存占用 |
|---------|---------|------|---------|
| 100点 | SMA | <0.1s | <10MB |
| 1,000点 | ES | <0.5s | <20MB |
| 10,000点 | LT | <2s | <50MB |

## 🔄 迭代计划

### v1.1.0 (计划中)
- [ ] 支持ARIMA模型
- [ ] 支持Prophet模型接口
- [ ] 添加季节性检测功能
- [ ] 支持多时间序列同时预测

### v1.2.0 (计划中)
- [ ] 添加Web界面
- [ ] 支持API服务模式
- [ ] 添加更多评估指标
- [ ] 支持模型自动选择

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 开源协议

本项目采用 MIT 开源协议 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- 灵感来源：Google TimesFM、Meta Prophet
- 致敬所有开源贡献者

---

<p align="center">
  如果这个项目对您有帮助，请给我们一个 ⭐️
</p>
