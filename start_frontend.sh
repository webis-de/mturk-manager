#!/usr/bin/env bash

cd "$(dirname "$0")"

docker-compose -f frontend/docker-compose.yml up