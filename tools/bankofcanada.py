import io
import requests
import pandas as pd
from datetime import date


class ExchangeRateParser:
    DAILY_EXCHANGE_RATE_URL = r'http://www.bankofcanada.ca/valet/observations/group/FX_RATES_DAILY/csv?start_date=%s&end_date=%s'

    @staticmethod
    def _get_csv(url):
        r = requests.get(url)

        # Read only the OBSERVATIONS section
        observations_started = False
        observations_finished = False
        stream = io.StringIO()
        for line in r.text.splitlines():
            if not observations_started:
                observations_started = (line == 'OBSERVATIONS')
            if not observations_finished:
                observations_finished = (observations_started and len(line) == 0)
            if observations_started and not observations_finished:
                stream.write(line+'\n')

        # rewind stream
        stream.seek(0)
        return stream

    @staticmethod
    def _get_dataframe(stream):
        df = pd.read_csv(stream, skiprows=1, index_col=0, parse_dates=True)
        df.fillna(method='bfill', inplace=True)
        return df

    def parse(self):
        start_date = date(date.today().year, 1, 1).strftime('%Y-%m-%d')
        end_date = date.today().strftime('%Y-%m-%d')
        url = self.DAILY_EXCHANGE_RATE_URL % (start_date, end_date)
        with self._get_csv(url) as stream:
            df = self._get_dataframe(stream)
            return df
