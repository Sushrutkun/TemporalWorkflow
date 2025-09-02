#!/bin/sh
set -e

# Start Temporal server in background
temporal server start \
  --frontend-port 7233 \
  --ui-port 8233 \
  --disable-metrics \
  --dynamic-config-value frontend.enableUpdateWorkflowExecution=false &

# Wait a bit for server to boot
sleep 5

# Start worker and client in background
python3 workflow.py &
python3 client.py &

# Keep container alive until one of them stops
wait -n
