# Data

Before training CNN and Yolov7 models, you must make dataset.

## 1. Installation
Install packages with:
```
pip install -r requirements.txt
```

## 2. Module
### 2.1 Download Stock OHLCV historical data
download stock historical data using [FinanceDataReader](https://github.com/financedata-org/FinanceDataReader)

```
# download all stock historical data of both kospi and kosdaq markets
python make_stocks.py -m kospi kosdaq
```

Download Directory

```
Data
├── Stock
│   ├── Kosdaq
│       ├── 000250.csv
│       └── ...
│   └── Kospi
│       ├── 000020.csv
│       └── ...
```

### 2.2 Make Candlestick Chart
make candlestick chart from stock historical data

__Select market, base style, and the number of tickers__
```
# make candlestick chart of both kospi and kosdaq markets in Yolo folder based on yolo default setting
python make_candlesticks -n Yolo -m kospi kosdaq --yolo

# make candlestick chart of only kospi market in CNN folder based on cnn default setting
python make_candlesticks -n CNN -m kospi --cnn

# make only 50 tickers
python make_candlesticks -n Yolo -m kospi kosdaq --yolo -num 50
```

__Add Feature__
```
# with volume
python make_candlesticks -n CNN -m kospi kosdaq --cnn -v

# with Simple Moving Average (period 10 and 20)
python make_candlesticks -n CNN -m kospi kosdaq --cnn -sma 10 20

# with Exponential Moving Average (period 60 and 120)
python make_candlesticks -n CNN -m kospi kosdaq --cnn -ema 60 120

# with Moving Average Convergence & Divergence (short period 12, long period 26, signal period 9)
python make_candlesticks -n CNN -m kospi kosdaq --cnn -macd 12 26 9
```

__Adjust chart setting__
```
# trading period 250, image size 1600 × 500
python make_candlesticks -n Yolo -m kospi kosdaq --yolo --period 250 --size 1600 500
```
### 2.3 Update
### 2.4 Labeling
### 2.5 Make Dataset

```python
import 
```