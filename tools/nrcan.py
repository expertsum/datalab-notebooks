import requests
import pandas as pd
import warnings
from bs4 import BeautifulSoup
from datetime import date

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


class GasPriceParser:
    MONTREAL_GAS_PRICE_URL = r'http://www2.nrcan.gc.ca/eneene/sources/pripri/prices_bycity_e.cfm?productID=1&' \
                             r'locationID=28&frequency=D&priceYear=%s&Redisplay='

    @staticmethod
    def _get_html(url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        prices_table = soup.find('table', id='pricesTable')
        return str(prices_table)

    @staticmethod
    def _get_dataframe(html):
        df_list = pd.read_html(html, parse_dates=True)
        df = df_list[0]
        #df.drop(df.columns[[5, 6, 7, 8]], axis=1, inplace=True) <- It doesn't work anymore.
        df.columns = df.columns.droplevel([0, 1, 2])
        df.columns = ['Date', 'Price', 'Taxes', 'MarketingMargin', 'RefiningMargin']
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        return df

    def parse(self):
        url = self.MONTREAL_GAS_PRICE_URL % (date.today().year)
        html = self._get_html(url)
        df = self._get_dataframe(html)
        return df
