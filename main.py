from math import ceil
from datetime import datetime, timedelta

from pandas import DataFrame
from matplotlib import style

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from app.db.connection import session
from app.db.models import Post


def get_posts(ts_from, ts_to):
    '''Retrieve all posts by given time filter'''

    posts = (session.query(Post)
             .filter(Post.created_at
                     .between(ts_from, ts_to))).all()

    if posts:
        posts_df = DataFrame(list(map(lambda post: post.to_dict(), posts)))
        posts_df.set_index('created_at', inplace=True)

        # group every 30 minuts
        MINUTES_30 = '30T'
        return posts_df.resample(MINUTES_30).count()


def plots(posts_df, graph_type='bar'):
    _df.plot()
    plt.show()


def predict(time=None):
    DAYS = 20

    a =  datetime(2018,6,1,2,55)
    b = a + timedelta(days=DAYS)

    posts = get_posts(a, b)

    posts['day'] = posts['time'].apply(lambda x: x.day).astype(float)
    posts['hour'] = posts['time'].apply(lambda x: x.hour).astype(float)
    posts['minute'] = posts['time'].apply(lambda x: x.minute).astype(float)

    PERCENT_TO_PREDICT = 40

    c = posts['count'].values.reshape((len(posts['count']), 1))

    forecast_col = 'count'
    forecast_out = int(ceil( (PERCENT_TO_PREDICT / 100) * len(posts)))

    posts['label'] = posts[forecast_col].shift(-forecast_out)

    clean_data = posts.dropna()
    clean_data.set_index('time', inplace=True)


    X = np.array(clean_data.drop(['label', 'count'], 1))

    scaler = MinMaxScaler()
    scaler.fit(X)
    X = scaler.transform(X)

    X_lately= X[-forecast_out:]

    clean_data = clean_data.dropna()
    y = np.array(clean_data['label'])

    x_t, x_test, y_t, y_test = train_test_split(X, y, shuffle=False, test_size=.2)

    ln = LinearRegression()
    ln.fit(x_t, y_t)
    accuracy = ln.score(x_test, y_test)

    return ln.predict(time)
    # accuracy = ln.score(x_test, y_test)
    # forecast_set = ln.predict(X_lately)

    # return accuracy
