#!/usr/bin/env bash

ssh-keygen -t rsa -b 4096 -f jwtRS256.key
# Пароль не устанавливать!
openssl rsa -in jwtRS256.key -pubout -outform PEM -out jwtRS256.key.pub
cat jwtRS256.key
cat jwtRS256.key.pub