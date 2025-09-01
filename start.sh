#!/bin/sh
# Start Temporal dev server in background
temporal server start-dev --ip 0.0.0.0 --port 7233 &

# Wait a bit for Temporal to boot
sleep 5

# Run your client/workflow code
python3 workflow.py
python3 client.py
