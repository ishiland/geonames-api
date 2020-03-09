#!/bin/sh

while ! nc -z db 5432 2>/dev/null; do
  echo "Waiting for geonames database..."
  sleep 1
done

python3 manage.py run --host 0.0.0.0 --port 5000
