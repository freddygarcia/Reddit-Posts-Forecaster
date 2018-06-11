from app.util import add_30_minutes
from pandas import DataFrame
from app.db.connection import session
from app.db.models import Post


def get_posts(ts_from, ts_to):
    '''Retrieve all posts by given time filter'''

    posts = (session.query(Post)
             .filter(Post.created_at
                     .between(ts_from, ts_to))).all()

    if posts:
        posts_df = DataFrame(list(map(lambda post: post.to_dict(), posts)))
        calc = []

        # perform a 30-minutes-grouping
        while ts_from < ts_to:

            ts_from_plus_30_min = add_30_minutes(ts_from)

            # counts posts in 30 minutes range
            count = posts_df.loc[
                (posts_df['created_at'] >= ts_from)
                & (posts_df['created_at'] < ts_from_plus_30_min)
            ].shape[0]

            calc.append((ts_from, count))

            ts_from = add_30_minutes(ts_from)

        return DataFrame(calc, columns=['time', 'count'])


def plots(df):
    # TODO
    df.set_index('time', inplace=True)

    df.plot()

    plt.show()


def predict(ts):
    # TODO
    pass    
