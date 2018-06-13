'''
All related to download y save posts from reddit.

Request is performed and then parsed with beautifulsoup.
Parsed data is stored using the app.persistence module.
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


def save_last(last):
    with open('last.txt', 'w+') as f:
        f.write(last)


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

    if after: save_last(str(after))

    ref_name = data[-1]['created_utc']
    pull_data(ref_name)



def run_loop(self, times=2, delay=1):
    """ Run 'task' some many times"""

    i = 0

    while i < times:

        # run task
        self.pull_data()
        self.save_data()

        # increment count
        i += 1

        # wait a while
        time_sleep(delay)
