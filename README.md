# ecommerce reporter
project for web programming 298.
uses an automated collector to check two ecommerce sites once an hour.
adds info about these deals to a redis database.
uses a flask server to query the database for its most recent deals.

dependencies (installed)
-
Requests, BeautifulSoup4, flask,
    redis, pytest

usage
-
0. Confirm all shell scripts are executable
    >chmod +x *.sh
1. Open first terminal
2. Run start_redis shell script in first terminal
    >source start_redis.sh
3. Open second terminal
4. Run start_flask shell script in second terminal
    >source start_flask.sh
5. Open third terminal
6. Run start_collector shell script in third terminal
7.  >source start_collector.sh
8. The collector will scrape the websites for data. If the current deals
 have changed, it will update the Redis database. If it has not, it will
 check again in 1 hour.
 
flask_server.py
-
contains functions to start a flask server that queries an extant redis db

collector.py
-
scrapes the BJJHQ and MMAHQ websites for new deals once an hour using
requests and updates the redis db if deals have changed.