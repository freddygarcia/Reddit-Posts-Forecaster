from datetime import datetime

from app.db.connection import session
from app.db.models import Post


def save_post(permalink, created_at):
    '''Define the way to persist the post data'''

    post = Post(permalink=permalink,
                created_at=created_at)
    session.add(post)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        print(f'error catched : {permalink}')


def save_posts(posts_list):
    for post in posts_list:
        created_utc = datetime.utcfromtimestamp(post['created_utc'])

        post = Post(permalink=post['permalink'],
                    created_at=created_utc)
        session.add(post)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        print(f'error catched : {str(e)}')
