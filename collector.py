import requests
import time
from redis import Redis
from bs4 import BeautifulSoup

class DailyDeal:
    """
    a class holding a deal's name, price, and sport.

    params:
        str name
        int price
        str sport

    constructs:
        DailyDeal
    """
    def __init__(self, name, price, sport):
        self.name = name
        self.price = price
        self.sport = sport
    

def update_db(r, deal):
    """
    pushes a DailyDeal's price, name, and sport members onto the front of the
        redis lists associated with those values.

    params:
        DailyDeal deal

    returns:
        void
    """
    r.lpush('product_price', deal.price)
    r.lpush('product_name', deal.name)
    r.lpush('product_sport', deal.sport)


def collect_deal(url, sport):
    """
    creates a DailyDeal from a provided URL.

    params:
        str url
        str sport

    returns:
        DailyDeal
    """
    # Request a GET response from the URL, then check if successful
    response = requests.get(url)
    response.raise_for_status()

    # Get data from the provided URL's elements
    try:
        soup = BeautifulSoup(response.text, "html.parser")
        name = soup.find('h1').text.strip()
        # Replace dollar sign for type casting to prevent decoding errors,
        # then cast as int
        price = int(soup
                    .find('div', id="buyBox")
                    .find('div', id="buyButton")
                    .find('em')
                    .text.replace('$', ''))
    # If it cannot find the proper elements on the webpage, the webpage is
    # not a supported URL for our program and should return a None instead
    # of a DailyDeal.
    except AttributeError:
        print("Invalid URL: {}".format(url))
        return None

    return DailyDeal(name, price, sport)


def deal_has_changed(r, deal):
    """
    queries the redis database for the most recent deal of the same sport
        and returns whether or not the deal has changed.

    if there are not yet deals for that sport, returns that the deal has
        changed in order to trigger the database update.

    params:
        DailyDeal deal

    returns:
        bool
    """
    counter = int(0)
    # If there are no products in the db, return True
    try:
        most_recent_product_sport = r.lindex('product_sport', counter).decode()
    except AttributeError:
        return True

    # Iterate across values until product type is the same
    while most_recent_product_sport != deal.sport:
        counter += 1
        # If only 1 product in the db and has a different type, return True
        try:
            most_recent_product_sport = r.lindex('product_sport', counter)\
                .decode()
        except AttributeError:
            return True

    # Get most recent product name of same sport
    most_recent_product_name = r.lindex('product_name', counter).decode()

    return deal.name != most_recent_product_name


def run_collector():
    """
    the automatic collector for the daily deals on http://bjjhq.com/ and
        http://mmahq.com/.
    checks the sites every 15 minutes and updates if the deals have changed
        for the respective sports.
    """
    r = Redis(host='localhost', port=6379, db=0)

    while True:
        # Checks the sites once an hour
        bjj_deal = collect_deal('http://www.bjjhq.com/', 'bjj')
        if deal_has_changed(r, bjj_deal):
            update_db(r, bjj_deal)

        mma_deal = collect_deal('http://www.mmahq.com/', 'mma')
        if deal_has_changed(r, mma_deal):
            update_db(r, mma_deal)

        time.sleep(3600)

