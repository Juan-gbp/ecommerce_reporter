from redis import Redis
#https://www.bjjhq.com/
import requests
from bs4 import BeautifulSoup

r = Redis(host='localhost', port=6379)

class MyClass:
  def __init__(self, name = '', price = 0):
    self.name = name
    self.price = price
  
  def set_price(self, price):
    self.price = price
    
  def set_name(self, name):
    self.name = name
    

def update_db():
    response = requests.get('https://www.bjjhq.com/')

    soup = BeautifulSoup(response.text, "html.parser")
    # for later
    # soup = soup.find('div', id="outerDiv").find('div', id="main").find('div', id="Panel1")
    # soup = soup.find('div', id="fullWidthWrapper").find('div', id="wrapper").find('div', id="container")
    name = soup.find('h1').text
    soup = soup.find('div', id="buyBox").find('div', id="buyButton")
    # Replace dollar sign for type casting
    price = soup.find('em').text.replace('$', '')

    iter1 = MyClass()
    iter1.set_price(price)
    iter1.set_name(name)

    r.set('Price', iter1.price)
    r.set('Name', iter1.name)
