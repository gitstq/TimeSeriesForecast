# 📖 TimeSeriesForecast 使用指南

## 📚 目錄

- [🎯 專案介紹](#🎯-專案介紹)
- [📦 安裝](#📦-安裝)
- [🚀 快速開始](#🚀-快速開始)
- [💡 詳細用法](#💡-詳細用法)
- [📊 支援的模型](#📊-支援的模型)
- [🎨 資料格式](#🎨-資料格式)
- [🔧 高級配置](#🔧-高級配置)
- [📝 範例](#📝-範例)
- [❓ 常見問題](#❓-常見問題)

---

## 🎯 專案介紹

**TimeSeriesForecast** 是一款專為開發者、資料分析師和業務人員設計的輕量級時間序列預測CLI工具。

### ✨ 核心特點

- 🔌 **零依賴** - 純Python標準庫，無需安裝任何外部包
- ⚡ **一鍵預測** - 簡單命令完成資料載入、建模、預測全流程
- 📊 **多模型支援** - 整合5種常用預測模型
- 🎨 **視覺化輸出** - ASCII藝術圖表 + 可選Matplotlib高品質圖表
- 🔧 **靈活配置** - 支援自訂預測週期、信賴區間、模型參數
- 📦 **開箱即用** - pip安裝即可，無需複雜配置

---

## 📦 安裝

### 環境要求

- Python 3.8 或更高版本
- 無需安裝任何外部依賴（零依賴設計）

### 安裝方式

#### 方式1: pip安裝（推薦）

```bash
pip install TimeSeriesForecast
```

#### 方式2: 從原始碼安裝

```bash
git clone https://github.com/gitstq/TimeSeriesForecast.git
cd TimeSeriesForecast
pip install -e .
```

#### 方式3: 直接使用（無需安裝）

```bash
python forecast.py run data.csv --model sma --period 30
```

---

## 🚀 快速開始

### 1. 準備資料

建立CSV檔案，格式如下：

```csv
date,value
2024-01-01,100
2024-01-02,120
2024-01-03,115
2024-01-04,130
...
```

### 2. 執行預測

```bash
# 使用簡單移動平均模型預測未來30天
forecast run data.csv --model sma --period 30

# 使用指數平滑模型
forecast run data.csv --model es --alpha 0.3 --period 30

# 比較多個模型
forecast compare data.csv --models sma,es,lt --period 30

# 生成預測圖表
forecast plot data.csv --output forecast.png --period 60
```

### 3. 查看結果

程式會輸出：
- 📊 預測趨勢ASCII圖表
- 📈 預測值表格（包含信賴區間）
- 📉 模型評估指標（RMSE、MAE、MAPE）

---

## 💡 詳細用法

### 基本命令

```bash
# 執行預測
forecast run <file> [OPTIONS]

# 比較多個模型
forecast compare <file> [OPTIONS]

# 生成圖表
forecast plot <file> [OPTIONS]

# 查看幫助
forecast --help
forecast info
```

### 主要選項

| 選項 | 簡寫 | 說明 | 預設值 |
|------|------|------|--------|
| `--model` | `-m` | 預測模型 | sma |
| `--period` | `-p` | 預測週期數 | 30 |
| `--window` | `-w` | 移動平均窗口大小 | 7 |
| `--alpha` | `-a` | 指數平滑alpha值 | 0.3 |
| `--no-plot` | - | 不顯示圖表 | False |
| `--output` | `-o` | 保存結果到檔案 | - |

---

## 📊 支援的模型

### 1. 簡單移動平均 (SMA) ⭐推薦

```
forecast run data.csv --model sma --window 7 --period 30
```

**適用場景**：短期資料平滑、雜訊消除
**參數**：
- `--window`：窗口大小，越大越平滑

### 2. 加權移動平均 (WMA)

```
forecast run data.csv --model wma --window 7 --period 30
```

**適用場景**：趨勢跟隨、近期資料更重要
**參數**：
- `--window`：窗口大小

### 3. 指數平滑 (ES)

```
forecast run data.csv --model es --alpha 0.3 --period 30
```

**適用場景**：中期預測、考慮歷史權重
**參數**：
- `--alpha`：平滑係數 (0-1)，越大越重視近期資料

### 4. 線性趨勢 (LT)

```
forecast run data.csv --model lt --period 30
```

**適用場景**：線性增長/下降資料
**特點**：自動擬合線性趨勢

### 5. 簡單回歸 (SR)

```
forecast run data.csv --model sr --max-degree 2 --period 30
```

**適用場景**：多項式趨勢、複雜關係
**參數**：
- `--max-degree`：多項式最高次數

### 模型比較

```bash
# 自動比較多個模型並排名
forecast compare data.csv --models sma,es,lt,sr --top-k 3
```

輸出範例：

```
📊 模型排名 (按RMSE):
   1. es - RMSE: 5.2342
   2. lt - RMSE: 6.1234
   3. sma - RMSE: 7.5678
```

---

## 🎨 資料格式

### 支援的格式

#### 1. CSV檔案（推薦）

```csv
date,value
2024-01-01,100
2024-01-02,120
2024-01-03,115
```

自動識別列名：
- 日期列：`date`, `time`, `timestamp`, `datetime`
- 數值列：`value`, `y`, `close`, `price`, `amount`

#### 2. JSON檔案

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

#### 3. JSON Lines檔案

```jsonl
{"date": "2024-01-01", "value": 100}
{"date": "2024-01-02", "value": 120}
```

### 指定列名

如果自動識別失敗，可手動指定：

```bash
forecast run data.csv --date-col my_date --value-col my_value
```

---

## 🔧 高級配置

### 資料預處理

#### 缺失值填充

```bash
# 線性插值（預設）
forecast run data.csv --fill-method linear

# 前向填充
forecast run data.csv --fill-method forward

# 後向填充
forecast run data.csv --fill-method backward

# 均值填充
forecast run data.csv --fill-method mean

# 填充為0
forecast run data.csv --fill-method zero
```

#### 異常值處理

自動處理3倍IQR以外的異常值

### 輸出格式

```bash
# 保存為JSON
forecast run data.csv --output result.json --format json

# 保存為CSV
forecast run data.csv --output result.csv --format csv

# 保存為Markdown
forecast run data.csv --output result.md --format markdown
```

### 圖表生成

#### ASCII圖表（預設，無需額外依賴）

```bash
forecast run data.csv --no-plot
```

#### Matplotlib圖表（需要安裝matplotlib）

```bash
# 先安裝matplotlib
pip install matplotlib

# 生成PNG圖表
forecast plot data.csv --output forecast.png --period 60

# 自訂尺寸
forecast plot data.csv --output forecast.png --width 1200 --height 800
```

---

## 📝 範例

### 範例1：銷售資料預測

```bash
# 準備資料 sales.csv
# date,amount
# 2024-01-01,5000
# 2024-01-02,5500
# ...

# 執行預測
forecast run sales.csv --model es --alpha 0.3 --period 30 --output sales_forecast.json
```

### 範例2：股票價格預測

```bash
# 使用線性趨勢模型
forecast run stock.csv --model lt --period 90

# 比較多個模型
forecast compare stock.csv --models sma,es,lt --period 90 --top-k 2
```

### 範例3：網站訪問量預測

```bash
# 使用移動平均模型
forecast run traffic.csv --model sma --window 7 --period 30

# 生成趨勢圖
forecast plot traffic.csv --output traffic_forecast.png --period 30
```

### 範例4：API呼叫量預測

```bash
# 使用指數平滑
forecast run api_calls.csv --model es --alpha 0.5 --period 60 --output api_forecast.json
```

---

## ❓ 常見問題

### Q1: 安裝失敗？

**A**: 確保Python版本>=3.8，並使用pip最新版本：

```bash
pip install --upgrade pip
pip install TimeSeriesForecast
```

### Q2: 資料載入失敗？

**A**: 檢查資料格式：
- 確保CSV/JSON檔案編碼為UTF-8
- 確保日期列和數值列存在且正確
- 使用`--date-col`和`--value-col`指定列名

### Q3: 預測結果不準確？

**A**: 嘗試以下方法：
1. 增加歷史資料量
2. 選擇合適的模型（使用`compare`命令比較）
3. 調整模型參數（如alpha、window）
4. 檢查資料是否有異常值

### Q4: 如何處理季節性資料？

**A**: 對於季節性資料，建議：
1. 使用指數平滑模型（ES）
2. 分解季節性成分
3. 考慮使用Prophet等專用工具

### Q5: 命令列提示"command not found"？

**A**: 確保安裝成功：
```bash
pip show TimeSeriesForecast
```

如果未找到，嘗試：
```bash
python -m forecast run data.csv --model sma --period 30
```

### Q6: 如何獲取更詳細的日誌？

**A**: 使用調試模式：
```bash
forecast --debug run data.csv --model sma --period 30
```

---

## 📞 技術支援

- 📋 Issue: https://github.com/gitstq/TimeSeriesForecast/issues
- 📖 文件: https://github.com/gitstq/TimeSeriesForecast#readme
- 💬 討論: https://github.com/gitstq/TimeSeriesForecast/discussions

---

<p align="center">
  ⭐ 如果這個專案對您有幫助，請給我們一個星標！
</p>
