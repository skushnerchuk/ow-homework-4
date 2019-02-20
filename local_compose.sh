#!/usr/bin/env bash

docker-compose -f local-compose.yml down
docker build -t airtradex_protect_local .
docker-compose -f local-compose.yml up -d