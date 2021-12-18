# !/bin/sh

cd /var/app

deactivate
python -m venv .venv
source .venv/bin/acticate

pip install -r requirements.txt