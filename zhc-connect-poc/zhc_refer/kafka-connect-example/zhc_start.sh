
./bin/kafka-topics --create --zookeeper 192.168.99.100:2181 --replication-factor 1 --partitions 1 --topic test

./bin/kafka-console-producer --broker-list 192.168.99.100:29092 --topic TextLinesTopic

{"id": 999, "product": "foo", "quantity": 100, "price": 50}