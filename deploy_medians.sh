#!/usr/bin/env bash

cd "$(dirname "$0")"

set -e

rm -rf venv
python3.6 -m venv venv
source venv/bin/activate
pip install --upgrade pip

pip3 install -r requirements.txt
python3.6 run_script_deploy_medians.py