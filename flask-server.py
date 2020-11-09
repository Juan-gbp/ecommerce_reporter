import sys, flask, redis
from flask import Flask, jsonify
from redis import Redis

# redis-server must already be running
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


app.run(host='127.0.0.1')
sys.exit()
