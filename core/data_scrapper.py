import pandas as pd
from price_loaders.tradingview import load_asset_price
import pytz 
from warnings import filterwarnings

from logger import logger 
filterwarnings('ignore')

#features = ['Max_Price', 'Min_Price', 'Open_price', 'Close_Price']


def get_last_period(symbol: str, period: int, tf: int, to_csv=False):
    '''Get a csv file with data of the specified symbol for a certain period
    
    symbol: Stock data short symbol ('AAPL', 'BTCUSDT')
    period: Specify the candles count
    tf: Candle timeframe

    Returns:
    df: pandas dataframe with loaded symbol data
    '''
    logger.info('Try to access tradingview...')

    df = load_asset_price(symbol, period, str(tf), pytz.timezone('UTC'))
    logger.info(f'Data consumed, total rows: {df.shape}')
    df['time'] = df['time'].apply(lambda x: str(x).split('+')[0])
    df['time'] = pd.to_datetime(df['time'])
    df.rename(columns={'time':'Time', 'open':'Open_Price', 'high':'Max_Price', 
                       'low':'Min_Price', 'close':'Close_Price', 'volume':'Volume'}, inplace=True)
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')
    df.set_index(['Time'], inplace=True)

    logger.info(f'Data configured, total rows: {df.shape}')

    if to_csv:
        df.to_csv(f'{symbol}_{period}_{tf}.csv', index=True)

    return df