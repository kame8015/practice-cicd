# !/bin/sh

sudo su -

source ~/.bashrc

cd /opt/app

rm -rf .venv/

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt