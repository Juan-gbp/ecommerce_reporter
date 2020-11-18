from redis import Redis
#https://www.bjjhq.com/
import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.bjjhq.com/')


soup = BeautifulSoup(response.text, "html.parser")

soup = soup.find('div', id="outerDiv").find('div', id="main").find('div', id="Panel1")
soup = soup.find('div', id="fullWidthWrapper").find('div', id="wrapper").find('div', id="container")
name = soup.find('h1').text
soup = soup.find('div', id="buyBox").find('div', id="buyButton")
price = soup.find('em').text


r = Redis(host='localhost', port=6379, db=0)

class MyClass:
  def __init__(self, name = '', price = 0):
    self.name = name
    self.price = price
  
  def set_price(self, price):
    self.price = price
    
  def set_name(self, name):
    self.name = name
    

iter1 = MyClass()
iter1.set_price(price)
iter1.set_name(name)

r.set('Price', iter1.price)

print(r.get('Price'))
