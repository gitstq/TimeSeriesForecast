# 📖 TimeSeriesForecast ユーザーガイド

## 📚 目次

- [🎯 プロジェクト紹介](#🎯-プロジェクト紹介)
- [📦 インストール](#📦-インストール)
- [🚀 クイックスタート](#🚀-クイックスタート)
- [💡 詳細な使用方法](#💡-詳細な使用方法)
- [📊 サポートされるモデル](#📊-サポートされるモデル)
- [🎨 データ形式](#🎨-データ形式)
- [🔧 高度な設定](#🔧-高度な設定)
- [📝 例](#📝-例)
- [❓ よくある質問](#❓-よくある質問)

---

## 🎯 プロジェクト紹介

**TimeSeriesForecast** は、開発者、データアナリスト、ビジネスユーザーに設計された軽量な時系列予測CLIツールです。

### ✨ 主な特徴

- 🔌 **ゼロ依存** - 純粋なPython標準ライブラリ、外部パッケージ不要
- ⚡ **ワンボタン予測** - シンプルなコマンドでデータ読み込み、モデル構築、予測を実行
- 📊 **複数モデル対応** - 5つの組み込み予測モデル
- 🎨 **視覚化出力** - ASCIIアートチャート + オプションのMatplotlib高品質チャート
- 🔧 **柔軟な設定** - 予測期間、信頼区間、モデルパラメータのカスタマイズ
- 📦 **すぐ使える** - pipでインストール、複雑な設定不要

---

## 📦 インストール

### 必要環境

- Python 3.8以上
- 外部依存なし（ゼロ依存設計）

### インストール方法

#### 方法1: pipでインストール（推奨）

```bash
pip install TimeSeriesForecast
```

#### 方法2: ソースからインストール

```bash
git clone https://github.com/gitstq/TimeSeriesForecast.git
cd TimeSeriesForecast
pip install -e .
```

#### 方法3: 直接使用（インストール不要）

```bash
python forecast.py run data.csv --model sma --period 30
```

---

## 🚀 クイックスタート

### 1. データ準備

CSVファイルを作成：

```csv
date,value
2024-01-01,100
2024-01-02,120
2024-01-03,115
2024-01-04,130
...
```

### 2. 予測実行

```bash
# 単純移動平均モデルで予測
forecast run data.csv --model sma --period 30

# 指数平滑モデルを使用
forecast run data.csv --model es --alpha 0.3 --period 30

# 複数モデルを比較
forecast compare data.csv --models sma,es,lt --period 30

# 予測チャートを生成
forecast plot data.csv --output forecast.png --period 60
```

### 3. 結果の確認

以下が出力されます：
- 📊 予測トレンドのASCIIチャート
- 📈 予測値テーブル（信頼区間付き）
- 📉 モデル評価指標（RMSE、MAE、MAPE）

---

## 💡 詳細な使用方法

### 基本コマンド

```bash
# 予測実行
forecast run <ファイル> [オプション]

# モデル比較
forecast compare <ファイル> [オプション]

# チャート生成
forecast plot <ファイル> [オプション]

# ヘルプ表示
forecast --help
forecast info
```

### 主なオプション

| オプション | 省略形 | 説明 | デフォルト |
|------------|--------|------|-----------|
| `--model` | `-m` | 予測モデル | sma |
| `--period` | `-p` | 予測期間数 | 30 |
| `--window` | `-w` | 移動平均ウィンドウサイズ | 7 |
| `--alpha` | `-a` | 指数平滑alpha値 | 0.3 |
| `--no-plot` | - | チャートを表示しない | False |
| `--output` | `-o` | 結果をファイルに保存 | - |

---

## 📊 サポートされるモデル

### 1. 単純移動平均 (SMA) ⭐推奨

```
forecast run data.csv --model sma --window 7 --period 30
```

**適用場面**：短期データの平滑化、ノイズ低減
**パラメータ**：
- `--window`：ウィンドウサイズ、大きいほど平滑

### 2. 加重移動平均 (WMA)

```
forecast run data.csv --model wma --window 7 --period 30
```

**適用場面**：トレンド追跡、直近データ更重要
**パラメータ**：
- `--window`：ウィンドウサイズ

### 3. 指数平滑 (ES)

```
forecast run data.csv --model es --alpha 0.3 --period 30
```

**適用場面**：中期予測、過去の重み考慮
**パラメータ**：
- `--alpha`：平滑化係数 (0-1)、大きいほど直近データ重視

### 4. 線形トレンド (LT)

```
forecast run data.csv --model lt --period 30
```

**適用場面**：線形増加/減少データ
**特徴**：線形トレンドを自動フィッティング

### 5. 単純回帰 (SR)

```
forecast run data.csv --model sr --max-degree 2 --period 30
```

**適用場面**：多項式トレンド、複雑な関係
**パラメータ**：
- `--max-degree`：多項式の最大次数

### モデル比較

```bash
# 複数モデルを自動比較・ランキング
forecast compare data.csv --models sma,es,lt,sr --top-k 3
```

出力例：

```
📊 モデルランキング (RMSE順):
   1. es - RMSE: 5.2342
   2. lt - RMSE: 6.1234
   3. sma - RMSE: 7.5678
```

---

## 🎨 データ形式

### サポート形式

#### 1. CSVファイル（推奨）

```csv
date,value
2024-01-01,100
2024-01-02,120
2024-01-03,115
```

自動検出される列名：
- 日付列：`date`, `time`, `timestamp`, `datetime`
- 値列：`value`, `y`, `close`, `price`, `amount`

#### 2. JSONファイル

```json
[
  {"date": "2024-01-01", "value": 100},
  {"date": "2024-01-02", "value": 120}
]
```

または

```json
{
  "data": [
    {"date": "2024-01-01", "value": 100}
  ]
}
```

#### 3. JSON Linesファイル

```jsonl
{"date": "2024-01-01", "value": 100}
{"date": "2024-01-02", "value": 120}
```

### 列名の指定

自動検出が失敗する場合は手動で指定：

```bash
forecast run data.csv --date-col my_date --value-col my_value
```

---

## 🔧 高度な設定

### データ前処理

#### 欠損値補完

```bash
# 線形補間（デフォルト）
forecast run data.csv --fill-method linear

# 前方補間
forecast run data.csv --fill-method forward

# 後方補間
forecast run data.csv --fill-method backward

# 平均値補間
forecast run data.csv --fill-method mean

# 0で補間
forecast run data.csv --fill-method zero
```

#### 外れ値処理

IQRの3倍以外の外れ値を自動処理

### 出力形式

```bash
# JSONで保存
forecast run data.csv --output result.json --format json

# CSVで保存
forecast run data.csv --output result.csv --format csv

# Markdownで保存
forecast run data.csv --output result.md --format markdown
```

### チャート生成

#### ASCIIチャート（デフォルト、追加依存なし）

```bash
forecast run data.csv --no-plot
```

#### Matplotlibチャート（matplotlib必要）

```bash
# matplotlibをインストール
pip install matplotlib

# PNGチャート生成
forecast plot data.csv --output forecast.png --period 60

# カスタムサイズ
forecast plot data.csv --output forecast.png --width 1200 --height 800
```

---

## 📝 例

### 例1: 売上データ予測

```bash
# データ準備 sales.csv
# date,amount
# 2024-01-01,5000
# 2024-01-02,5500
# ...

# 予測実行
forecast run sales.csv --model es --alpha 0.3 --period 30 --output sales_forecast.json
```

### 例2: 株価予測

```bash
# 線形トレンドモデル使用
forecast run stock.csv --model lt --period 90

# 複数モデル比較
forecast compare stock.csv --models sma,es,lt --period 90 --top-k 2
```

### 例3: Webサイトアクセス予測

```bash
# 移動平均モデル使用
forecast run traffic.csv --model sma --window 7 --period 30

# トレンドチャート生成
forecast plot traffic.csv --output traffic_forecast.png --period 30
```

### 例4: API呼び出し予測

```bash
# 指数平滑使用
forecast run api_calls.csv --model es --alpha 0.5 --period 60 --output api_forecast.json
```

---

## ❓ よくある質問

### Q1: インストールに失敗しました？

**A**: Pythonバージョン>=3.8、最新pipを使用してください：

```bash
pip install --upgrade pip
pip install TimeSeriesForecast
```

### Q2: データの読み込みに失敗しました？

**A**: データ形式を確認：
- CSV/JSONファイルのエンコーディングがUTF-8か確認
- 日付列と値列が存在し正しいか確認
- `--date-col`と`--value-col`で列名を指定

### Q3: 予測結果の精度が悪い？

**A**: 以下を試してください：
1. 履歴データ量を増やす
2. 適切なモデルを選択（`compare`コマンド使用）
3. モデルパラメータを調整（alpha、windowなど）
4. データに外れ値がないか確認

### Q4: 季節性データは怎么处理？

**A**: 季節性データには以下を推奨：
1. 指数平滑モデル（ES）使用
2. 季節性成分の分解
3. Prophetなどの専門ツールを検討

### Q5: 「command not found」と出た？

**A**: インストール確認：
```bash
pip show TimeSeriesForecast
```

見つからない場合：
```bash
python -m forecast run data.csv --model sma --period 30
```

### Q6: 詳細なログを取得したい？

**A**: デバッグモード使用：
```bash
forecast --debug run data.csv --model sma --period 30
```

---

## 📞 サポート

- 📋 イシュー: https://github.com/gitstq/TimeSeriesForecast/issues
- 📖 ドキュメント: https://github.com/gitstq/TimeSeriesForecast#readme
- 💬 ディスカッション: https://github.com/gitstq/TimeSeriesForecast/discussions

---

<p align="center">
  ⭐ このプロジェクトが役に立ったら、星をください！
</p>
