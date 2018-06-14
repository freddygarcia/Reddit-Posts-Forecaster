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
