import sys
from flask import Flask, jsonify
from redis import Redis
from dummy_collector import *


# redis-server process must already be running for this to work
# if there is no data in the redis db, this will yell at you
def flask_server_start():
    app = Flask(__name__)
    r = Redis(host='localhost', port=6379)

    @app.route('/count', methods=['GET'])
    def get_count():
        count = r.get('count').decode()
        return jsonify({'count': count})

    @app.route('/increment', methods=['POST'])
    def increment():
        r.incr('count')
        return r.get('count')

    @app.route('/deal', methods=['GET'])
    def get_deal():
        update_db()
        name = r.get('Name').decode()
        price = r.get('Price').decode()
        return jsonify({'name': name, 'price': price})

    app.run(host="127.0.0.1", port=5001)


flask_server_start()
sys.exit()
