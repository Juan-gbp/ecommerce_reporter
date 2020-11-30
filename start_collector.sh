#! /bin/bash

source $(pwd)/venv/bin/activate

python3 - <<'EOF'
from collector import run_collector
run_collector()
EOF