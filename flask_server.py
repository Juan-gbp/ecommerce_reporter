import sys
from flask import Flask, jsonify
from redis import Redis


# redis-server process must already be running for this to work
# if there is no data in the redis db, this will yell at you
def flask_server_start():
    app = Flask(__name__)
    r = Redis()

    @app.route('/count', methods=['GET'])
    def get_count():
        count = r.get('count').decode()
        return jsonify({'count': count})

    @app.route('/increment', methods=['POST'])
    def increment():
        r.incr('count')
        return r.get('count')

    app.run(host="127.0.0.1")


flask_server_start()
sys.exit()
