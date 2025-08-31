FROM temporalio/server:latest

EXPOSE 7233

CMD ["temporal", "server", "start-dev", "--ip", "0.0.0.0"]
