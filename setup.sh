#!/bin/bash
# do necessary inital tasks

git pull
git submodule update --recursive --remote --init

pip3 install -r requirements.txt

cd ./mturk

if [ $OSTYPE = "msys" ]; then
	command="python"
else
	command="python3"
fi

$command manage.py createcachetable
$command manage.py migrate