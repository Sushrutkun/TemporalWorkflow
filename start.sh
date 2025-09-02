#!/bin/sh
set -e

# Start Temporal dev server in background (UI + gRPC on chosen ports)
TEMPORAL_UI_PORT=8233 \
TEMPORAL_CLI_ADDRESS=0.0.0.0:7233 \
temporal server start-dev --no-metrics &

# Wait a bit for server to boot
sleep 5

# Start worker and client in background
python3 workflow.py &
python3 client.py &

# Keep container alive
wait -n
