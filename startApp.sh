#!/bin/bash

docker compose -f docker-compose.yml up -d --build

(cd ./api-services && docker compose up -d --build)