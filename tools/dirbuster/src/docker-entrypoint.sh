#!/bin/sh

set -eu

source .venv/bin/activate
python3 dirbuster.py "${@}"