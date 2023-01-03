import argparse
from pathlib import Path
import multiprocessing as mp
import parmap
import numpy as np
import sys
p = Path.absolute(Path.cwd().parent)
sys.path.append(str(p))
from Data.stock import StockMarket, Stock
from Data.candlestick import CNNChart, YoloChart, CandlstickChart
import warnings
warnings.filterwarnings(action='ignore')

def make_ticker_candlesticks(tickers, chart: CandlstickChart, market, start='2006', end='a'):
    for ticker in tickers:
        data = Stock(ticker, market).load_data()
        dates = data.index.tolist()
        dates = [d for d in dates if (d >= start) & (d < end)]
        for last_date in dates:
            chart.make_chart(ticker, last_date)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '--name', '-n', type=str, dest='name', default=None, help='the name of chart folder'
    )
    parser.add_argument(
        '--root', '-r', type=str, default=str(Path.cwd()), help='Root Directory of Stock' 
    )
    parser.add_argument(
        '--exist-ok', action='store_true',
        help='existing project/name ok, do not increment'
    )
    parser.add_argument(
        '--market', '-m', nargs='+', type=str, dest='market', required=True,
        help='You can input a market under options\n' + \
             'KOSPI: Stock market includes KOSPI only\n' + \
             'KOSDAQ: Stock market includes KOSDAQ only\n' + \
             'KONEX: Stock market includes KONEX only'
    )
    parser.add_argument(
        '--number', '-num', type=int, dest='number', default=None,
        help='How many stock you make',
    )
    parser.add_argument(
        '--start', '-s', type=str, default='2006', help='Make chart that trade date >= start'
    )
    parser.add_argument(
        '--end', '-e', type=str, default='a', help='Make chart that trade date < end'
    )
    
    base = parser.add_mutually_exclusive_group(required=True)
    base.add_argument(
        '--yolo', action='store_true', help='use default yolo chart setting'
    )
    base.add_argument(
        '--cnn', action='store_true', help='use default cnn chart setting'
    )
    
    config = parser.add_argument_group('Chart Configure')
    config.add_argument(
        '--size', nargs='+', type=int, dest='size', default=argparse.SUPPRESS, help='the size of chart image'
    )
    config.add_argument(
        '--period', type=int, default=argparse.SUPPRESS, help='the trading period of a chart'
    )
    config.add_argument(
        '--linespace', '-ls', type=float, default=argparse.SUPPRESS, help='the distance of each candle'
    )
    config.add_argument(
        '--candlewidth', '-cw', type=float, default=argparse.SUPPRESS, help='the width of each candle'
    )
    config.add_argument(
        '--linewidth', '-lw', type=float, default=argparse.SUPPRESS, help='the width of moving averages'
    )
    config.add_argument(
        '--style', type=str, default=argparse.SUPPRESS,
        help='plot style of matplotlib (ex. default: white background, dark_style: dark background)'
    )
    
    feature = parser.add_argument_group('Feature')
    feature.add_argument(
        '--volume', '-v', action='store_true', default=argparse.SUPPRESS, help='chart with volume'
    )
    feature.add_argument(
        '--SMA', '-sma', nargs='+', type=int, default=argparse.SUPPRESS, help='the list of Simple Moving Average period list'
    )
    feature.add_argument(
        '--EMA', '-ema', nargs='+', type=int, default=argparse.SUPPRESS, help='the list of Exponential Moving Average period list'
    )
    feature.add_argument(
        '--MACD', '-macd', nargs='+', type=int, default=argparse.SUPPRESS, help='MACD short period, long period, signal period'
    )
    
    color = parser.add_argument_group('Color')
    color.add_argument(
        '--UpColor', '-uc', type=str, default=argparse.SUPPRESS, help='the color of bullish candlesticks'
    )
    color.add_argument(
        '--DownColor', '-dc', type=str, default=argparse.SUPPRESS, help='the color of bearish candlesticks'
    )
    color.add_argument(
        '--SMAColor', '-sc', nargs='+', type=str, default=argparse.SUPPRESS, help='the color of each SMA'
    )
    color.add_argument(
        '--EMAColor', '-ec', nargs='+', type=str, default=argparse.SUPPRESS, help='the color of each EMA'
    )
    color.add_argument(
        '--MACDColor', '-mc', nargs='+', type=str, default=argparse.SUPPRESS, help='the color of MACD and MACD oscillator'
    )
    args = parser.parse_args()
    
    kwargs = args.__dict__
    
    for market in args.market:
        tickers = StockMarket(market.upper()).tickers
        num = args.number if args.number else len(tickers)
        kwargs['market'] = market
        if args.cnn:
            chart = CNNChart(**kwargs)
        else:
            chart = YoloChart(**kwargs)
        
        num_cores = min(10, mp.cpu_count(), num)
        splited_tickers = np.array_split(tickers[:num], num_cores)
        splited_tickers = [x.tolist() for x in splited_tickers]
        
        parmap.map(
            make_ticker_candlesticks, splited_tickers,
            chart, market, args.start, args.end,
            pm_pbar=True,
            pm_processes=num_cores
        )
        kwargs['exist_ok'] = True