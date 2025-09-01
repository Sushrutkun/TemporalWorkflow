FROM debian:bullseye-slim

# Install dependencies
RUN apt-get update && apt-get install -y curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*

# Install Temporal CLI into /usr/local/bin
RUN curl -sSfL https://temporal.download/cli.sh | sh \
    && mv /root/.temporalio/bin/temporal /usr/local/bin/temporal

# Verify install
RUN temporal --version

EXPOSE 8233
CMD ["temporal", "server", "start-dev", "--ip", "0.0.0.0"]

