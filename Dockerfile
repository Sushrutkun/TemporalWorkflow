FROM temporalio/server:latest

EXPOSE 7233

# Run Temporal in dev mode (uses SQLite, no Cassandra/Postgres)
CMD ["temporal", "server", "start-dev", "--ip", "0.0.0.0", "--db-filename", "/tmp/temporal.db"]
