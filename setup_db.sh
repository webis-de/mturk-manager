#!/bin/bash
# do necessary inital tasks

git pull
# git submodule update --recursive --remote --init

pip3 install boto3
pip3 install xmltodict
pip3 install djangorestframework
pip3 install django-cors-headers
pip3 install psycopg2

# pip3 install -r requirements.txt

#cd ./mturk_db
#python3 manage.py migrate