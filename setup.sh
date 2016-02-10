#!/bin/bash
echo 'Installing Virtual Environment Tool'
sudo apt-get install python-virtualenv python3-dev
echo 'Creating Virtual Environment'
virtualenv --python=python3.4 venv
echo 'Installing requirements'
./venv/bin/pip3 install pip==7.1.2 --upgrade
./venv/bin/pip3 install setuptools==18.4 --upgrade
./venv/bin/pip3 install -r ./requirements.txt
