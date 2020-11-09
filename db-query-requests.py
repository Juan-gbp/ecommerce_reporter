import sys, redis, flask, requests
from redis import Redis

# flask-server must already be running
def main():

    localhost = '127.0.0.1'
    flask_port = str('5000')
    redis_port = str('6379')
    base_url = str('http://{}:{}'.format(localhost, flask_port))

    endpoint = str('count')
    url = str('{}/{}'.format(base_url, endpoint))

    response = requests.get('{}'.format(url))
    print(response)
    print(response.headers)
    print(response.json())


main()
sys.exit()
