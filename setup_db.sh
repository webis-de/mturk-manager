#!/bin/bash
# do necessary inital tasks

git pull
git submodule update --recursive --remote --init

pip3 install -r requirements.txt

cd ./mturk_db
python3 manage.py migrate