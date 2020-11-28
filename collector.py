import requests, time
from redis import Redis
from bs4 import BeautifulSoup

r = Redis(host='localhost', port=6379)

class DailyDeal:
    def __init__(self, name, price, sport):
        self.name = name
        self.price = price
        self.sport = sport
    

def update_db(deal):
    #r.llen(<listname>)
    # Use lpush so newest product is always added to the beginning
    r.lpush('product_price', deal.price)
    r.lpush('product_name', deal.name)
    r.lpush('product_sport', deal.sport)


def collect_deal(url):
    response = requests.get(url)
    response.raise_for_status()

    if 'bjj' in url.lower():
        sport = 'jiujitsu'
    elif 'mma' in url.lower():
        sport = 'mma'
    else:
        sport = None

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
    except AttributeError:
        print("Invalid URL: {}".format(url))
        return None

    return DailyDeal(name, price, sport)


def deal_has_changed(deal):
    counter = int(0)
    # If there are no products in the db, return True
    try:
        sport = r.lindex('product_sport', counter).decode()
    except AttributeError as e:
        print("No values exist in 'product_sport' list for product_sport"
              ": \"{}\".".format(deal.sport))
        return True

    # Iterate across values until product type is the same
    while sport != deal.sport:
        counter += 1
        # If only 1 product in the db and has a different type, return True
        try:
            sport = r.lindex('product_sport', counter).decode()
        except AttributeError as e:
            print("No values exist in 'product_sport' list for product_sport"
                  ": \"{}\".".format(deal.sport))
            return True

    # Get values of the most recent product of the same sport
    name = r.lindex('product_name', counter).decode()
    price = int(r.lindex('product_price', counter).decode())

    return deal.name != name and deal.price != price


while True:
    # Checks the sites every 15 minutes
    bjj_deal = collect_deal('http://www.bjjhq.com/')
    if deal_has_changed(bjj_deal):
        update_db(bjj_deal)

    mma_deal = collect_deal('http://www.mmahq.com/')
    if deal_has_changed(mma_deal):
        update_db(mma_deal)

    time.sleep(900)
