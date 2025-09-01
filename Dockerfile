FROM debian:bullseye-slim

# Install curl + unzip
RUN apt-get update && apt-get install -y curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*

# Install Temporal CLI (includes temporal server)
RUN curl -sSfL https://temporal.download/cli.sh | sh

# Expose Temporal gRPC port
EXPOSE 7233

# Run Temporal in dev mode (SQLite, no external DB)
CMD ["temporal", "server", "start-dev", "--ip", "0.0.0.0"]
