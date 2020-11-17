from redis import Redis

r = Redis(host='localhost', port=6379, db=0)

class MyClass:
  def __init__(self, name = '', price = 0):
    self.name = name
    self.price = price
  
  def set_price(self, price):
    self.price = price
    

iter1 = MyClass()
iter1.set_price(8)

r.set('Price', iter1.price)

print(r.get('Price'))