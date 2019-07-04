#!/usr/bin/env bash

docker container stop rabbitmq
docker container rm rabbitmq

docker run -d --hostname my-rabbit --name rabbitmq -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=password -p 5672:5672 -p 15672:15672 rabbitmq:3-management