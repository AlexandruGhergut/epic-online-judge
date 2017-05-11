#!/bin/bash
# wait-for-postgres.sh

set -e

export PGPASSWORD=$DB_PASSWORD
until psql -h $DB_HOST -U $DB_USER -e $DB_NAME -c '\l'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
