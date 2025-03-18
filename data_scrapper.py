import pandas as pd
from price_loaders.tradingview import load_asset_price
import pytz 
from warnings import filterwarnings

from logger import logger 
filterwarnings('ignore')

features = ['Max_Price', 'Min_Price', 'Open_price', 'Close_Price']


def get_last_period(symbol, period, tf, to_csv=True):
    logger.info('Try to access tradingview...')

    df = load_asset_price(symbol, period, str(tf), pytz.timezone('Etc/UTC'))
    df['time'] = df['time'].apply(lambda x: str(x).split('+')[0])
    df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S')
    df.rename(columns={'time':'Time', 'open':'Open_Price', 'high':'Max_Price', 
                       'low':'Min_Price', 'close':'Close_Price', 'volume':'Volume'}, inplace=True)
    df.set_index(['Time'], inplace=True)

    if to_csv:
        df.to_csv(f'{symbol}_{period}_{tf}.csv', index=True)

    return df