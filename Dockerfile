FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    ca-certificates \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install Temporal CLI
RUN curl -sSfL https://temporal.download/cli.sh | sh \
    && mv /root/.temporalio/bin/temporal /usr/local/bin/temporal \
    && chmod +x /usr/local/bin/temporal

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Copy application code
COPY . .

# Copy and set permissions for startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Create non-root user for security
RUN useradd -m -u 1000 temporaluser && \
    chown -R temporaluser:temporaluser /app
USER temporaluser

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose ports
EXPOSE 7233 8233

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8233/ || exit 1

# Start the application
CMD ["/start.sh"]