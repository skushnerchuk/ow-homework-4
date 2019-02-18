#!/usr/bin/env bash

docker-compose down
docker build -t airtradex_protect .
docker-compose up -d