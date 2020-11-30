#! /bin/bash

source $(pwd)/venv/bin/activate

python3 - <<'EOF'
from flask_server import flask_server_start
flask_server_start()
EOF