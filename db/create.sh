#!/bin/bash
set -e

echo "creating ${POSTGRES_DB}_test database"
createdb -U $POSTGRES_USER ${POSTGRES_DB}_test
psql -d ${POSTGRES_DB}_test -c 'create extension postgis;'