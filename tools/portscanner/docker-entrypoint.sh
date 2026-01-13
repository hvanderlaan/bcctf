#!/bin/sh

cd /app

if [ -d .venv ]; then
    source .venv/bin/activate
else
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
fi

python3 portscanner.py ${@}