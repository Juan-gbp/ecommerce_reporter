import sys
from flask import Flask, jsonify
from redis import Redis


def flask_server_start():
    """
    runs a flask server to interface with a redis database

    params:
        none

    returns:
        none
    """
    app = Flask(__name__)
    r = Redis(host='localhost', port=6379,db=0)

    @app.route('/deals', methods=['GET'])
    def get_deals():
        """
        queries a redis database and returns the most recent bjj and mma deals
            to the request as a json response

        params:
            none

        returns:
            json {{'name': str, 'price': int, 'sport' str},
                {'name': str, 'price': int, 'sport' str}}
            or
            json {}
        """
        responses = []

        # r.llen always returns an int
        num_deals = r.llen('product_name')

        if num_deals != 0:
            name = r.lindex('product_name', 0).decode().strip()
            price = int(r.lindex('product_price', 0).decode().strip())
            sport = r.lindex('product_sport', 0).decode().strip()

            responses.append({'name': name, 'price': price, 'sport': sport})

            if num_deals > 1:
                other_sport = 'mma' if sport == 'bjj' else 'bjj'

                ctr = 1
                while ctr < num_deals:
                    sport = r.lindex('product_sport', ctr)\
                        .decode().strip()

                    if sport == other_sport:
                        other_name = r.lindex('product_name', ctr)\
                            .decode().strip()
                        other_price = int(r.lindex('product_price', ctr)
                                          .decode().strip())

                        responses.append({'name': other_name,
                                          'price': other_price,
                                          'sport': other_sport})
                        break
                    ctr += 1

        return jsonify(responses)

    app.run(host="127.0.0.1", port=5001)
    sys.exit()
