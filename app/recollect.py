'''
this file is a helper to retrieve massive entries for
Reddit from pushshift api
'''

from time import sleep as time_sleep
from json import loads as json_loads
from requests import get
from app.db.persistence import save_posts

HEADERS = {
    'User-Agent': 'osx:r/relationships.multiple.results:v1.0 (by /u/freddie'
}

URL = ('https://api.pushshift.io/reddit/search/submission/'
       '?filter=permalink,created_utc,title&size=1000&subreddit=AskReddit')


def perform_request(url):
    text_data = get(url, headers=HEADERS).text
    json = json_loads(text_data)
    return json['data']


def pull_data(i = 10, after=None):

    time_sleep(2)

    if i == 0: return
    i -= 1

    print(f' i => {i}')

    url = f'{URL}&before={after}' if after else URL

    data = perform_request(url)

    save_posts(data)

    ref_name = data[-1]['created_utc']
    pull_data(i, ref_name)
