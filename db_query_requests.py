import requests

# flask-server must already be running
def db_query():

    localhost = '127.0.0.1'
    flask_port = str('5000')
    redis_port = str('6379')
    base_url = str('http://{}:{}'.format(localhost, flask_port))

    endpoint = str('count')
    url = str('{}/{}'.format(base_url, endpoint))

    response = requests.get('{}'.format(url))

    return response
