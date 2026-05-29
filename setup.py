# TimeSeriesForecast

Zero-dependency time series forecasting CLI tool.

## Installation

```bash
pip install TimeSeriesForecast
```

## Quick Start

```bash
# Run prediction
forecast run data.csv --model sma --period 30

# Compare models
forecast compare data.csv --models sma,es,lt --period 30

# Generate chart
forecast plot data.csv --output forecast.png --period 60
```

## License

MIT
