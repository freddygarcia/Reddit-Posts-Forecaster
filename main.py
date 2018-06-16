from pandas import DataFrame
import matplotlib.pyplot as plt

from app.db.connection import session
from app.db.models import Post


def get_posts(ts_from=None, ts_to=None):
    '''Retrieve all posts by given time filter.

    I just want ts_from to be optional, but
    if parameters were inverted, may be confusing.
    '''

    if not (ts_from or ts_to): return None

    query = session.query(Post)
    posts = None

    if ts_from:
        posts = (query.filter(Post.created_at
                .between(ts_from, ts_to))).all()
    else:
        posts = query.filter(Post.created_at < ts_to).all()

    if posts:
        posts_df = DataFrame(list(map(lambda post: post.to_dict(), posts)))
        posts_df.set_index('created_at', inplace=True)

        # group every 30 minutes
        MINUTES_30 = '30T'
        return posts_df.resample(MINUTES_30).count()

    return DataFrame()


def plots(posts_df):
    posts_df.plot()
    plt.show()


def predict(ts):
    '''Give the aprox number of posts between `ts` and `ts + 1 hour`
    using data that has `created_at < ts`.

    All the details is in app.prediction module

    Parameters
    ----------
    ts : datetime
        date to predict the number of posts

    Returns
    -------
    int
        the number of posts between ts and ts + 1 hour
    '''
    from app.prediction import Forecaster

    train, test = Forecaster.train_test_data(ts)
    forecaster = Forecaster.forecaster(train)

    return forecaster.predict(ts)

