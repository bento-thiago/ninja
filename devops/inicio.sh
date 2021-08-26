#!/bin/bash
cd /home/thiagobento/ninja/devops/exercicios/app
docker rm -f $(docker ps -a -q)
docker volume rm $(docker volume ls)
docker-compose -f docker-compose.yml up -d
