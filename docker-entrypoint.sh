#!/bin/sh
cd /notification
pip install -r requirements.txt
echo "requirements installed"
echo "start notification service"
stdbuf -oL python -u main.py