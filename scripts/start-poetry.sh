#!/bin/sh
# start-poetry.sh

set -e

cmd="$@"

# Activate environment
. /app/venv/bin/activate

>&2 echo "Starting poetry..."
exec $cmd
