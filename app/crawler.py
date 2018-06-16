'''
All related to download y save posts from reddit.

Request is performed and then parsed with beautifulsoup.
Parsed data is stored using the app.persistence module.
'''

from requests import get
from bs4 import BeautifulSoup
from app.util import aprox_time
from app.db.persistence import save_post
from time import sleep as time_sleep

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'
                  ' AppleWebKit/537.36 (KHTML,like Gecko) Chrome/3'
                  '9.0.2171.95 Safari/537.36'
}


class Crawler:
    """ Pull down data from reddit and persist them"""

    def __init__(self):
        self.divs = []
        self.last_permalink = ''

    def pull_data(self):
        """Pull posts from reddit"""

        # perform the request sending headers as a browser
        response = get('https://www.reddit.com/r/AskReddit/new/', headers=HEADERS)

        page = response.text
        soup = BeautifulSoup(page, 'html.parser')
        self.divs = soup.find_all('div', {'class': 'Post'})

        if not self.divs:
            # sometimes, happend to give a bad response (1 of 4 times)
            # if we couldn't get any records, look for posts again
            self.pull_data()

    def save_data(self):
        """ Store reddit posts"""

        # short function to get the permalink from our base div
        get_permalink = lambda div: div.find('a', {'class': 'SQnoC3ObvgnGjWt90zD9Z'})['href']
        
        # this var will let us know when we can start to
        # save records, cause we dont want to insert duplicates
        can_save = False

        for div in reversed(self.divs):
            # for convenience, insert rows in desc order

            text_time = div.find('a', {'class': '_3jOxDPIQ0KaOWpzvSQo-1s'}).text
            created_at = aprox_time(text_time)
            permalink = get_permalink(div)

            if can_save:
                # if previous record was same as saved in last run,
                # start to save
                save_post(permalink, created_at)

            if permalink == self.last_permalink \
               or self.last_permalink == '':
                # when self.last_permalink is empty, script is running for first time
                can_save = True

        if self.divs:
            # remember the first row (in our case, as we inverted the array, the last)
            # so next time running we can compare for avoiding duplicates
            self.last_permalink = get_permalink(self.divs[0])


    def pull_save_data(self, times=2, delay=1):
        """ Perform pull and data some

        Parameters
        ----------
        times: int
            How many times loop will run

        delay: int
            Delay in seconds for performing requests
        """

        i = 0

        while i < times:

            # run task
            self.pull_data()
            self.save_data()

            # increment count
            i += 1

            # wait a while
            time_sleep(delay)
