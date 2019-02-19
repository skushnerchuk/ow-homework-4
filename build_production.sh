#!/usr/bin/env bash

docker login -u registry -p VFERGUSON11284registry registry.sk-developer.ru:5043
docker build -t registry.sk-developer.ru:5043/airtradex_protect:latest .
docker push registry.sk-developer.ru:5043/airtradex_protect
docker logout registry.sk-developer.ru:5043