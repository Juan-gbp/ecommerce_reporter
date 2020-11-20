import sys
import os
from db_query_requests import db_query

# The redis-server service, the flask_server.py script, and the
# collector must be run prior to running this
def main():
    # Query the server through the requests
    response = db_query()
    print(response)
    print(response.headers)
    print(response.json())
    # Stop redis services

    os.system("redis-cli shutdown")


if __name__ == '__main__':
    main()

sys.exit()
