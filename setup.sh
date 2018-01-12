#!/bin/bash
# do necessary inital tasks

git submodule init
git submodule update --remote

mkdir venv
python3 -m venv venv

source venv/bin/activate

pip install django==2.0
pip install whoosh==2.7.4
pip install xmltodict
pip install boto3
pip install secrets

cd ./mturk
python3 manage.py createcachetable
python3 manage.py makemigrations viewer mturk_manager
python3 manage.py migrate