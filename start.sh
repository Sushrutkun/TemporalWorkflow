#!/bin/sh
set -e

# Get the port from environment variable or use default
PORT=${PORT:-8233}

echo "Starting Temporal server on port $PORT..."

# Start Temporal dev server in background
temporal server start-dev \
    --ip 0.0.0.0 \
    --ui-port $PORT \
    --port 7233 \
    --headless \
    --db-filename /tmp/temporal.db \
    --dynamic-config-value frontend.enableClientVersionCheck=false &

# Store the PID of the temporal server
TEMPORAL_PID=$!

# Wait for Temporal server to be ready
echo "Waiting for Temporal server to start..."
sleep 15

# Check if Temporal is running
if ! kill -0 $TEMPORAL_PID 2>/dev/null; then
    echo "Temporal server failed to start"
    exit 1
fi

echo "Temporal server started successfully"

# Start worker in background
echo "Starting worker..."
python3 workflow.py &
WORKER_PID=$!

# Wait a bit for worker to start
sleep 5

# Start client to create schedule
echo "Starting client to create schedule..."
python3 client.py &
CLIENT_PID=$!

# Function to cleanup on exit
cleanup() {
    echo "Shutting down..."
    kill $TEMPORAL_PID $WORKER_PID $CLIENT_PID 2>/dev/null || true
    exit 0
}

# Set trap for cleanup
trap cleanup TERM INT

# Keep container alive and monitor processes
echo "All services started. Monitoring..."
while true; do
    if ! kill -0 $TEMPORAL_PID 2>/dev/null; then
        echo "Temporal server died, restarting..."
        exit 1
    fi
    if ! kill -0 $WORKER_PID 2>/dev/null; then
        echo "Worker died, restarting..."
        python3 workflow.py &
        WORKER_PID=$!
    fi
    sleep 10
done