'''
1. CNN Labeling

1.1 n%_01_2 Labeling
    only certain rising date is set to '1'
    - 0: close price declines
    - 1: close price rises more than 4 percent


2. Yolo Labeling

2.1 MinMax Labeling
    find minimum and maximum close date and halve a section. Repeat this.
    - 0: date when close price is maximum in section
    - 1: date when close price is minimum in section

2.2 Pattern Labeling
    5 Bullish candlestick pattern and 5 Bearish candlestick pattern
    - 0 ~ 4: Bullish candlestick pattern
    - 5 ~ 9: Bearish candlestick pattern

2.3 Merge Labeling
    Base on MinMax Labeling, write ovelapped Pattern Labeling (0: bullish, 1: bearish)
    - 0: 0 Label in MinMax Labeling
    - 1: 1 Label in MinMax Labeling

'''
import pandas as pd
from pathlib import Path
from stock import Stock
from utils import dataframe_empty_handler
from minmax_labeling import minmax_labeling
from pattern_labeling import pattern_labeling


class Labeling:
    def __init__(self, method, period) -> None:
        '''
        method: str
            the method of labeling
            CNN: n%_01_2
            Yolo: MinMax, Pattern, Merge
        period: int
            trading period (= the number of candlestick chart candles)
            input n period stock data to model
        '''
        self.path = Path.cwd() / 'Labeling'
        self.method = method
        self.period = period
    
    def process_labeling(self):
        pass
    
    def load_labeling(self):
        pass
    

class CNNLabeling(Labeling):
    def __init__(self, period, interval, method='4%_01_2') -> None:
        '''
        interval: int
            forecast interval
            predict n interval after the last input period
        
        Method
        1. n%_01_2
            1: after interval, if close price increase more than n%
            0: after interval, if close price decrease
        '''
        super().__init__(method, period)
        self.path = self.path / 'CNN' / self.method
        self.interval = interval
       
    def process_labeling(self, ticker, market='ALL'):
        super().process_labeling()
        stock = Stock(ticker, market)
        data = stock.load_data()
        dates = data.index.tolist()
        
        rows = [self.load_labeling()]
        for i in range(len(data)):
            section = data.iloc[i: i + self.period, :]  # trading(input) data
            try:
                forecast = data.iloc[i + self.period + self.interval - 1, :]  # forecast answer data
            except IndexError:
                break
            
            starting = 0
            endvalue = 0
            label = ""
            
            if len(section) == self.period:
                if self.method[1:] == "%_01_2":
                    starting = section.iloc[-1, 'Close']
                    endvalue = forecast['Close']
                    
                    if endvalue >= (1 + (int(self.method[0])/100)) * starting:
                        label = 1
                    elif endvalue < starting:
                        label = 0
                    else:
                        continue

                else:
                    return
                
                row = pd.DataFrame({
                    'Date': [dates[i]],
                    'Ticker': [ticker],
                    'Label': [label]
                })
                rows.append(row)
            
        labeling = pd.concat(rows)
        labeling.to_csv(self.path / f'labeling_{self.period}_{self.interval}.csv', index=False)
    
    @dataframe_empty_handler
    def load_labeling(self):
        super().load_labeling()
        labeling = pd.read_csv(self.path / f'labeling_{self.period}_{self.interval}.csv', index_col=0)
        self.labeling = labeling
        return labeling


class YoloLabeling(Labeling):
    def __init__(self, method, period) -> None:
        super().__init__(method, period)
        self.path = self.path / 'Yolo' / self.method
        
        
    def process_labeling(self, ticker, market='ALL'):
        super().process_labeling()
        stock = Stock(ticker, market)
        data = stock.load_data()
        dates = data.index.tolist()
        
        for i in range(len(data)):
            section = data.iloc[i: i + self.period, :]  # trading(input) data
            if len(section) == self.period:
                if self.method == 'MinMax':
                    labeling = minmax_labeling(section, self.period, 10)
                
                elif self.method == 'Pattern':
                    labeling = pattern_labeling(section)
                
                elif self.method == 'Merge':
                    return
            else:
                break
            
            labeling.to_csv(self.path / f'{ticker}_{dates[i]}.csv', index=False)


    @dataframe_empty_handler
    def load_labeling(self, ticker, trade_date):
        super().load_labeling()
        labeling = pd.read_csv(self.path / f'{ticker}_{trade_date}.csv', index_col=0)
        self.labeling = labeling
        return labeling