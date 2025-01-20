#!/usr/bin/env bash
# wait-for-it.sh

# Timeout in seconds
TIMEOUT=30
# Interval between checks
INTERVAL=1

# The host and port to wait for
HOST="$1"
PORT="$2"

# The command to run when the service is available
shift 2
CMD="$@"

# Function to check if the PostgreSQL service is available using pg_isready
wait_for() {
    until pg_isready -h "$HOST" -p "$PORT"; do
        echo "Waiting for $HOST:$PORT to be available..."
        sleep "$INTERVAL"
    done
    echo "$HOST:$PORT is available."
}

# Run the wait-for function with the given host and port
wait_for

# Run the command passed to the script
exec $CMD