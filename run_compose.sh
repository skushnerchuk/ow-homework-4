#!/usr/bin/env bash

docker-compose down
docker build -t airtradex_protect_local .
docker-compose up -d