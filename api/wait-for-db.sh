#!/bin/sh
set -e

host="$1"
shift
cmd="$@"

echo "Waiting for Postgres at $host..."

# Wait until Postgres is ready
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 2
done

>&2 echo "Postgres is up - executing command: $cmd"
exec $cmd
