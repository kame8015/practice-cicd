# !/bin/sh

sudo su -

cd /opt/app

rm -rf .venv/

python --version
python3 --version

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt