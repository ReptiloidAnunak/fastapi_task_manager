#!/bin/bash

echo "Starting database and API..."
docker compose up -d tasks_db tasks_api

echo "Waiting for API to be ready..."
sleep 15

echo "Running tests..."
docker compose run --rm tests

echo "Tests completed!"

docker compose down --remove-orphans
docker compose up -d --build
docker compose logs -f