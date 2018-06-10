from datetime import timedelta
from app.db.connection import session
from app.db.models import Post
from pandas import DataFrame


def save_post(permalink, created_at, content=''):
    '''Define the way to persist the post data'''

    post = Post(permalink=permalink,
                content=content,
                created_at=created_at)
    session.add(post)

    try:
        session.commit()
    except Exception as e:
        # TODO
        print(e)


def time(ts):
    return ts.strftime('%H:%M:%S')


def add_30_minutes(ts):
    """Helper to add 30 minutes to a given time"""
    return ts + timedelta(minutes=30)


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

            calc.append((ts_from.strftime('%H:%M:%S'), count))

            ts_from = add_30_minutes(ts_from)

        return DataFrame(calc, columns=['time', 'count'])
