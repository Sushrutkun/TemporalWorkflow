FROM temporalio/auto-setup:latest

# Force Temporal to use SQLite instead of Cassandra/Postgres
ENV DB=sqlite
EXPOSE 7233

CMD ["temporal-server", "start-dev", "--ip", "0.0.0.0"]
