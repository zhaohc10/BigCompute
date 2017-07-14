#!/usr/bin/env bash

# 0) check remote topics on bn prod-green kafka cluster
docker run \
  --net=host \
  --rm confluentinc/cp-kafka \
  kafka-topics --describe --topic avro-events --zookeeper <zhc-kafka-cluster>

# 1) set up local kakfa cluster and enterprise version connect host
docker-compose -f zhc-connect-1-replicator.yml up -d


# 2) post the bn connector with avro converter to the connect host

docker-compose -f zhc-connect-1-replicator.yml exec connect-host-1 curl -X POST \
     -H "Content-Type: application/json" \
     --data '{
        "name": "bn-replicator-test-1",
        "config": {
          "connector.class":"io.confluent.connect.replicator.ReplicatorSourceConnector",
          "key.converter": "org.apache.kafka.connect.storage.StringConverter",
          "key.converter.schema.registry.url": "http://10.14.5.233:8081",
          "value.converter": "io.confluent.connect.avro.AvroConverter",
          "value.converter.schema.registry.url": "http://10.14.5.233:8081",
          "src.zookeeper.connect": "<zhc-kafka-cluster>2181",
          "src.kafka.bootstrap.servers": "<zhc-kafka-cluster>:9092",
          "dest.zookeeper.connect": "localhost:42181",
          "topic.whitelist": "avro-events",
          "topic.rename.format": "${topic}.replica"}}'  \
     http://localhost:28082/connectors



# 3) check the replica connector status connector on connect-host-1
docker-compose -f zhc-connect-1-replicator.yml  exec connect-host-1 curl -X GET http://localhost:28082/connectors/bn-replicator-test-1/status

# 4) check the replica topic on the target kafka cluster
docker run \
--net=host \
--rm confluentinc/cp-kafka \
kafka-topics --list --zookeeper localhost:42181

# 5) check the automatic created topic __.replica by replica connector on the dest-kafka-a
docker run \
  --net=host \
  --rm \
  confluentinc/cp-kafka \
  kafka-console-consumer --bootstrap-server localhost:9072 --topic avro-events.replica --new-consumer --from-beginning --max-messages 5

# 6) describe the automatic created topic __.replica by replica connector on the dest-kafka-a
docker run \
  --net=host \
  --rm confluentinc/cp-kafka \
  kafka-topics --describe --topic avro-events.replica --zookeeper localhost:42181
