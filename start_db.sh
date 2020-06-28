#!/usr/bin/env bash

cd "$(dirname "$0")"

docker-compose -f mturk_db/docker-compose.yml up -d db