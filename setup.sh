#!/bin/bash
# do necessary inital tasks

git submodule update --init

pip3 install -r corpus-viewer/requirements.txt
pip3 install -r requirements.txt

cd ./mturk
python3 manage.py createcachetable
python3 manage.py makemigrations viewer mturk_manager
python3 manage.py migrate