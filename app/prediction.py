from math import sqrt

from sklearn.metrics import mean_squared_error
from statsmodels.tsa.api import ExponentialSmoothing
import matplotlib.pylab as plt
import numpy as np
import pandas as pd

from main import get_posts


class Forecaster():
    '''Perform a forecast based on the stored posts data from reddit

    '''

    @staticmethod
    def train_test_data(ts, division_percent=.8):
        '''Retrieve data before `ts` to train and test our forecaster


        Parameters
        ----------
        ts : datetime
            Take posts data before `ts`

        division_percent: datetime (optional)
            Used to divide our data in train and test data

        Returns
        -------
        tuple
            the train and test data
        '''

        # make sure `division_percent` has a valid value
        division_percent = 1 if division_percent > 1 else division_percent
        division_percent = .8 if division_percent <= 0 else division_percent

        posts = get_posts(None, ts)

        DIVISION = int((len(posts.index)*division_percent))
        
        # divide data
        train = posts[:DIVISION]
        test = posts[DIVISION:]

        return train, test


    @staticmethod
    def forecaster(train_data, DATA_PERIOD=48):
        '''Gives a Forecaster instance based in the train_data.


        Parameters
        ----------
        train_data : dataframe
            Data to train our forecaster

        DATA_PERIOD: int (optional)
            The number of seasons to consider for the holt winters.

        Returns
        -------
        Forecaster
            Forecaster instance
        '''

        SEASONAL_PERIOD = DATA_PERIOD * 1

        # last date of records for reference
        model = ExponentialSmoothing(np.asarray(train_data.permalink),
                                    seasonal_periods=SEASONAL_PERIOD,
                                    trend='add',
                                    seasonal='add').fit()

        # Used to count steps starting from
        # that date.
        # The problem is that ExponentialSmoothing class
        # does no provide a clear api about how to use the 
        # `predict` method, so I have to add 30 minutes interval.
        base_date = train_data.index.max()

        return Forecaster(model, base_date)

    
    def __init__(self, model, base_date):
        self.model = model
        self.base_date = base_date


    def forecast(self, ts):
        '''Return an array of predictions from the `base_date`
        to `ts` plus an hour.

        Parameters
        ----------
        ts: datetime
            Gives predictions until `ts`

        Return
        ------
        np.array
             Array of predictions from the `base_date`
             to `ts` plus an hour
        '''

        # Given the difference between ts and the `base_date`.
        # The prediction array will go from `base_date` to `ts`
        # in 30 minutes interval PLUS two steps (one hour).
        DATE_DIFF = (ts - self.base_date)
        FORECAST_SIZE = round(DATE_DIFF.total_seconds() / 1800) + 2
        forecast_set = self.model.forecast(FORECAST_SIZE)

        return forecast_set


    def predict(self, ts):
        '''Given the `ts` return the prediction of how many post
            may be between `ts` and `ts + 1 hour` 

        '''
        forecast_set = self.forecast(ts)
        forecast_total = int(sum(forecast_set[-2:]))
        return forecast_total


    def score(self, test_data):
        '''Get how precise is how forecaster.

        Parameters
        ----------
        test_data: DataFrame
            Test data retrieved by `train_test_data` method

        Return
        ------
        float   
            Root mean square error, better while close to zero
        '''

        test_len = len(test_data.index)

        test_forecast = self.model.forecast(test_len)

        RMS = sqrt(mean_squared_error(test_data.permalink, test_forecast))

        return RMS


    def plot_forecaster(self, train, test):
        # Create data frame
        df = pd.DataFrame()
        df['date'] = pd.date_range(train.index.max(), periods=len(test.index), freq='30T')
        df.set_index('date', inplace=True)
        df['forecast'] = self.model.forecast(len(test.index))

        plt.figure(figsize=(16,8))
        plt.plot(train['permalink'], label='Train')
        plt.plot(test['permalink'], label='Test')
        plt.plot(df['forecast'], label='Forecast')
        plt.legend(loc='best')
        plt.show()  
