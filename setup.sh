#!/bin/bash
# do necessary inital tasks

if ! dpkg -l "python3-venv" &> /dev/null; then
# if ! python3 -c "import venv" &> /dev/null; then
    echo 'Please install python3-venv'
    exit
fi

# git submodule init
# git submodule update --remote

# mkdir venv
# python3 -m venv venv

# source venv/bin/activate

# pip install django==2.0
# pip install whoosh==2.7.4
# pip install xmltodict
# pip install boto3

# cd ./mturk
# python3 manage.py createcachetable
# python3 manage.py makemigrations viewer mturk_manager
# python3 manage.py migrate
