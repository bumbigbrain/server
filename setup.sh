#!/bin/bash


sudo apt update -y
sudo apt upgrade -y

sudo apt install python3-venv uvicorn stress-ng -y

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

