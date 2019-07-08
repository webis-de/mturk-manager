#!/usr/bin/env bash

cd ..

if [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
  /home/kritten/PycharmProjects/mturk-manager/venv/bin/celery -A mturk_db beat -l info
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
  ../venv/Scripts/celery -A mturk_db beat -l info
fi