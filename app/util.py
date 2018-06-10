''' Some helpers '''
from datetime import datetime, timedelta
from re import compile as re_compile
from time import sleep as time_sleep

re_search = re_compile(r'(\d{1,2}) (minute|minutes|hour|hours) ago')


def aprox_time(time_cad, now=datetime.now()):
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


def run_loop(task, times=2, delay=1):
    """ Run 'task' some many times"""

    i = 0

    while i < times:

        # run task
        task()

        # increment count
        i += 1

        # wait a while
        time_sleep(delay)
