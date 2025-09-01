FROM python:3.10-slim

# Install Temporal CLI
RUN apt-get update && apt-get install -y curl unzip ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -sSfL https://temporal.download/cli.sh | sh \
    && mv /root/.temporalio/bin/temporal /usr/local/bin/temporal

# Install Python dependencies
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Copy your repo code
COPY . /app
WORKDIR /app
ENV PYTHONPATH=/app

# Copy startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 7233 8233

CMD ["/start.sh"]
