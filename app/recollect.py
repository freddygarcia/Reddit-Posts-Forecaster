'''
this file is a helper to retrieve massive entries for
Reddit from pushshift api
'''

from datetime import datetime
from time import sleep as time_sleep
from json import loads as json_loads
from requests import get
from app.db.persistence import save_post

HEADERS = {
    'User-Agent': 'osx:r/relationships.multiple.results:v1.0 (by /u/freddie'
}

URL = ('https://api.pushshift.io/reddit/search/submission/'
       '?filter=permalink,created_utc,title&size=1000&subreddit=AskReddit')


def save_posts(posts):
    for post in posts:
        created_utc = datetime.utcfromtimestamp(post['created_utc'])
        save_post(post['permalink'], created_utc)


def perform_request(url):
    text_data = get(url, headers=HEADERS).text
    json = json_loads(text_data)
    return json['data']


def pull_data(after=None):

    time_sleep(2)

    url = f'{URL}&before={after}' if after else URL

    data = perform_request(url)

    save_posts(data)

    ref_name = data[-1]['created_utc']
    pull_data(ref_name)
