#!/usr/bin/env bash

cd "$(dirname "$0")"

docker-compose -f docker-compose.yml up -d db
#docker-compose -f docker-compose.yml up --build celery
#docker-compose -f docker-compose.yml up db
#docker-compose -f docker-compose.yml up db celery rabbitmq backend