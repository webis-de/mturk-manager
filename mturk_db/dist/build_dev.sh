#!/bin/bash
 
sudo docker build --build-arg branch=development --no-cache -t mturk-manager-global-db .