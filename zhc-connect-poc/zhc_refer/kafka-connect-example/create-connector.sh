#! /bin/bash

NAME=$1
TOPICS=$1

echo 'attempting post..'

# create the JDBC sink connector.
curl -X POST \
  -H "Content-Type: application/json" \
  --data '{"name": "'$NAME'", "config": { "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector", "tasks.max": 1, "connection.url": "jdbc:postgresql://localhost:7999/kafka?user=postgres&password=postgres", "topics": "'$TOPICS'", "poll.interval.ms": 1000, "auto.create": true, "auto.evolve": true } }' \
  http://192.168.99.100:8083/connectors
