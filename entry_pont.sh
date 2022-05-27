#!/bin/sh

docker stop $(docker ps -q)
docker rm $(docker ps -q -a)

docker-compose up --build