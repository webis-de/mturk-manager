#!/bin/bash
# do necessary inital tasks

git submodule init
git submodule update --remote

pip install -r requirements.txt

cd ./mturk
python3 manage.py createcachetable
python3 manage.py makemigrations viewer mturk_manager
python3 manage.py migrate