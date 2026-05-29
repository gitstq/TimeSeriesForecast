# 📖 TimeSeriesForecast User Guide

## 📚 Table of Contents

- [🎯 Project Introduction](#🎯-project-introduction)
- [📦 Installation](#📦-installation)
- [🚀 Quick Start](#🚀-quick-start)
- [💡 Detailed Usage](#💡-detailed-usage)
- [📊 Supported Models](#📊-supported-models)
- [🎨 Data Formats](#🎨-data-formats)
- [🔧 Advanced Configuration](#🔧-advanced-configuration)
- [📝 Examples](#📝-examples)
- [❓ FAQ](#❓-faq)

---

## 🎯 Project Introduction

**TimeSeriesForecast** is a lightweight time series forecasting CLI tool designed for developers, data analysts, and business users.

### ✨ Key Features

- 🔌 **Zero Dependencies** - Pure Python standard library, no external packages needed
- ⚡ **One-Click Prediction** - Simple commands to load data, train models, and forecast
- 📊 **Multiple Models** - 5 built-in forecasting models
- 🎨 **Visual Output** - ASCII art charts + optional Matplotlib high-quality charts
- 🔧 **Flexible Configuration** - Customizable forecast periods, confidence intervals, model parameters
- 📦 **Ready to Use** - Install via pip, no complex configuration required

---

## 📦 Installation

### Requirements

- Python 3.8 or higher
- No external dependencies required (zero-dependency design)

### Installation Methods

#### Method 1: pip install (Recommended)

```bash
pip install TimeSeriesForecast
```

#### Method 2: Install from source

```bash
git clone https://github.com/gitstq/TimeSeriesForecast.git
cd TimeSeriesForecast
pip install -e .
```

#### Method 3: Direct use (No installation)

```bash
python forecast.py run data.csv --model sma --period 30
```

---

## 🚀 Quick Start

### 1. Prepare Data

Create a CSV file with the following format:

```csv
date,value
2024-01-01,100
2024-01-02,120
2024-01-03,115
2024-01-04,130
...
```

### 2. Run Forecast

```bash
# Use Simple Moving Average model
forecast run data.csv --model sma --period 30

# Use Exponential Smoothing model
forecast run data.csv --model es --alpha 0.3 --period 30

# Compare multiple models
forecast compare data.csv --models sma,es,lt --period 30

# Generate forecast chart
forecast plot data.csv --output forecast.png --period 60
```

### 3. View Results

The program will output:
- 📊 ASCII trend chart
- 📈 Prediction table (with confidence intervals)
- 📉 Model evaluation metrics (RMSE, MAE, MAPE)

---

## 💡 Detailed Usage

### Basic Commands

```bash
# Run forecast
forecast run <file> [OPTIONS]

# Compare models
forecast compare <file> [OPTIONS]

# Generate chart
forecast plot <file> [OPTIONS]

# View help
forecast --help
forecast info
```

### Main Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--model` | `-m` | Forecasting model | sma |
| `--period` | `-p` | Number of periods to forecast | 30 |
| `--window` | `-w` | Moving average window size | 7 |
| `--alpha` | `-a` | Exponential smoothing alpha | 0.3 |
| `--no-plot` | - | Don't display chart | False |
| `--output` | `-o` | Save results to file | - |

---

## 📊 Supported Models

### 1. Simple Moving Average (SMA) ⭐Recommended

```
forecast run data.csv --model sma --window 7 --period 30
```

**Use Cases**: Short-term data smoothing, noise reduction
**Parameters**:
- `--window`: Window size, larger = smoother

### 2. Weighted Moving Average (WMA)

```
forecast run data.csv --model wma --window 7 --period 30
```

**Use Cases**: Trend following, recent data is more important
**Parameters**:
- `--window`: Window size

### 3. Exponential Smoothing (ES)

```
forecast run data.csv --model es --alpha 0.3 --period 30
```

**Use Cases**: Medium-term forecasting, considering historical weights
**Parameters**:
- `--alpha`: Smoothing factor (0-1), higher = more weight on recent data

### 4. Linear Trend (LT)

```
forecast run data.csv --model lt --period 30
```

**Use Cases**: Linear growth/decline data
**Features**: Automatically fits linear trend

### 5. Simple Regression (SR)

```
forecast run data.csv --model sr --max-degree 2 --period 30
```

**Use Cases**: Polynomial trends, complex relationships
**Parameters**:
- `--max-degree`: Maximum polynomial degree

### Model Comparison

```bash
# Automatically compare and rank multiple models
forecast compare data.csv --models sma,es,lt,sr --top-k 3
```

Sample output:

```
📊 Model Ranking (by RMSE):
   1. es - RMSE: 5.2342
   2. lt - RMSE: 6.1234
   3. sma - RMSE: 7.5678
```

---

## 🎨 Data Formats

### Supported Formats

#### 1. CSV File (Recommended)

```csv
date,value
2024-01-01,100
2024-01-02,120
2024-01-03,115
```

Auto-detects column names:
- Date column: `date`, `time`, `timestamp`, `datetime`
- Value column: `value`, `y`, `close`, `price`, `amount`

#### 2. JSON File

```json
[
  {"date": "2024-01-01", "value": 100},
  {"date": "2024-01-02", "value": 120}
]
```

Or

```json
{
  "data": [
    {"date": "2024-01-01", "value": 100}
  ]
}
```

#### 3. JSON Lines File

```jsonl
{"date": "2024-01-01", "value": 100}
{"date": "2024-01-02", "value": 120}
```

### Specifying Column Names

If auto-detection fails, specify manually:

```bash
forecast run data.csv --date-col my_date --value-col my_value
```

---

## 🔧 Advanced Configuration

### Data Preprocessing

#### Missing Value Imputation

```bash
# Linear interpolation (default)
forecast run data.csv --fill-method linear

# Forward fill
forecast run data.csv --fill-method forward

# Backward fill
forecast run data.csv --fill-method backward

# Mean fill
forecast run data.csv --fill-method mean

# Fill with zero
forecast run data.csv --fill-method zero
```

#### Outlier Handling

Automatically handles outliers beyond 3x IQR

### Output Formats

```bash
# Save as JSON
forecast run data.csv --output result.json --format json

# Save as CSV
forecast run data.csv --output result.csv --format csv

# Save as Markdown
forecast run data.csv --output result.md --format markdown
```

### Chart Generation

#### ASCII Chart (Default, No Extra Dependencies)

```bash
forecast run data.csv --no-plot
```

#### Matplotlib Chart (Requires matplotlib)

```bash
# Install matplotlib first
pip install matplotlib

# Generate PNG chart
forecast plot data.csv --output forecast.png --period 60

# Custom dimensions
forecast plot data.csv --output forecast.png --width 1200 --height 800
```

---

## 📝 Examples

### Example 1: Sales Data Forecasting

```bash
# Prepare data sales.csv
# date,amount
# 2024-01-01,5000
# 2024-01-02,5500
# ...

# Run forecast
forecast run sales.csv --model es --alpha 0.3 --period 30 --output sales_forecast.json
```

### Example 2: Stock Price Prediction

```bash
# Use Linear Trend model
forecast run stock.csv --model lt --period 90

# Compare multiple models
forecast compare stock.csv --models sma,es,lt --period 90 --top-k 2
```

### Example 3: Website Traffic Forecasting

```bash
# Use Moving Average model
forecast run traffic.csv --model sma --window 7 --period 30

# Generate trend chart
forecast plot traffic.csv --output traffic_forecast.png --period 30
```

### Example 4: API Calls Prediction

```bash
# Use Exponential Smoothing
forecast run api_calls.csv --model es --alpha 0.5 --period 60 --output api_forecast.json
```

---

## ❓ FAQ

### Q1: Installation failed?

**A**: Make sure Python version >= 3.8 and use the latest pip:

```bash
pip install --upgrade pip
pip install TimeSeriesForecast
```

### Q2: Data loading failed?

**A**: Check data format:
- Ensure CSV/JSON file encoding is UTF-8
- Ensure date and value columns exist and are correct
- Use `--date-col` and `--value-col` to specify column names

### Q3: Forecast results are inaccurate?

**A**: Try the following:
1. Increase historical data volume
2. Choose appropriate model (use `compare` command)
3. Adjust model parameters (e.g., alpha, window)
4. Check for outliers in data

### Q4: How to handle seasonal data?

**A**: For seasonal data, recommend:
1. Use Exponential Smoothing model (ES)
2. Decompose seasonal components
3. Consider using specialized tools like Prophet

### Q5: Command not found error?

**A**: Verify installation:
```bash
pip show TimeSeriesForecast
```

If not found, try:
```bash
python -m forecast run data.csv --model sma --period 30
```

### Q6: How to get detailed logs?

**A**: Use debug mode:
```bash
forecast --debug run data.csv --model sma --period 30
```

---

## 📞 Support

- 📋 Issues: https://github.com/gitstq/TimeSeriesForecast/issues
- 📖 Documentation: https://github.com/gitstq/TimeSeriesForecast#readme
- 💬 Discussions: https://github.com/gitstq/TimeSeriesForecast/discussions

---

<p align="center">
  ⭐ If this project helps you, please give us a star!
</p>
