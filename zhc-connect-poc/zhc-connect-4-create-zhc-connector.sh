#!/usr/bin/env bash

# 0) package our own connector
sbt clean
sbt pacakge

# 1) set up the kafka connector
docker-compose -f zhc-connect-4-zhc.yml up -d

# 2) create the topic and produce msg to to topic
./bin/kafka-topics --create --zookeeper localhost --replication-factor 1 --partitions 1 --topic avro-events
./bin/kafka-topics --list --zookeeper localhost

echo '{"id":"1234567890123456789","fields":["foo","bar"],"guid":"12345678-90ab-cdef-1234-567890abcdef","someother_id":"12345678"}' \
    | ./bin/kafka-console-producer --broker-list 192.168.99.100:9092 --topic  avro-events

./bin/kafka-console-consumer --bootstrap-server 192.168.99.100:9092 --topic  avro-events --from-beginning

# 3) check the connector create our own connectors using distributed mode
curl -XGET http://192.168.99.100:8083/connectors/

curl 192.168.99.100:8083/connectors -X POST -H'Content-type: application/json' -H'Accept: application/json' -d'{
  "name": "bn-own_connector-test-01",
  "config": {
    "topics": "avro-events",
    "connector.class": "io.bn.kafka.connect.MysqlSinkConnector",
    "tasks.max": 1,
    "host": "zhc-hahah"
  }
}'


# 4) check the console which should print out the changed msg on the logs
# eg:
# connect_1    | zhc hahaha{"id":"1234567890123456789","fields":["foo","bar"],"guid":"12345678-90ab-cdef-1234-567890abcdef","someother_id":"12345678"}

docker-compose -f zhc-connect-4-zhc.yml logs connect
