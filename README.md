# web_project_1
project for web_programming

dependencies (installed)
-
Requests, BeautifulSoup4, flask,
    redis, pytest, sys

flask_server.py
-
starts a flask server that queries an extant redis db

db_query_requests
-
queries the redis db thru the flask server using requests library 

Use
-
1. Open first terminal
2. Start Redis DB services
    >"redis-server"
3. Open second terminal
4. Start Flask server
    >"python3 ./flask_server.py" 
5. Open third terminal
6. Start Collector
