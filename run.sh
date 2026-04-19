#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install -r requirements.txt
docker compose up -d
python3 main.py
