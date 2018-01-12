#!/bin/bash
# do necessary inital tasks

git submodule init
git submodule update --remote

mkdir venv
python3 -m venv venv

source venv/bin/activate

pip install django==1.10.6
pip install whoosh==2.7.4