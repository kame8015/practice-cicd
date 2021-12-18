# !/bin/sh

cd /opt/app

python --version
which python
which python3

python -m venv .venv
source .venv/bin/acticate

pip install -r requirements.txt