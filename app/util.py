''' Some helpers '''
from datetime import datetime, timedelta
from re import compile as re_compile

from app.db.connection import session
from app.db.models import Post

re_search = re_compile(r'(\d{1,2}) (minute|minutes|hour|hours) ago')


def aprox_time(time_cad, now=None):
    '''
        Depending on the post time, take the moment when created

        if 'just now' in cad, give the current time,
        else, extract the time pattern assuming,
        by instance: 4 minutes ago, '{value} {unit} ago'

        if not cad given or empty, return current time

        Parameters
        ----------
        time_cad : str
            string containing when post was created

        now: datetime
            optional, it's for testing the function

        Returns
        -------
        datetime
            the aprox moment as datetime
    '''

    params = {}

    if not now:
        now = datetime.now()

    if time_cad is None \
       or'just now' in time_cad \
       or time_cad.strip() == '':
        return now

    regex_result = re_search.search(time_cad)

    value, unit = regex_result.groups()
    _value = int(value)

    if 'minute' in unit:
        params['minutes'] = _value

    elif 'hour' in unit:
        params['hours'] = _value

    return now - timedelta(**params)

def data_range():
    '''Retrive the current data range stored'''
    query = session.query(Post)

    get_date = lambda q: q.first().to_dict().get('created_at')

    p_max = get_date(query.order_by(Post.created_at.desc()))

    p_min = get_date(query.order_by(Post.created_at))

    return p_min, p_max