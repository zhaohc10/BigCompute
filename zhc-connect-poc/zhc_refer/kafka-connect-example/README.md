# Kafka Connect Example

A simple example of using Kafka Connect with Kafka Streams.

### Setup

1) Install Confluent on your company (needed for some of the scripts)

2) run `./kafka-start` to start docker containers

3) start the connectors by running:
- `./create-connector.sh test` 
- `./create-connector.sh test2`

4) run `mvn package` (to run it from the command line.)

5) Run `TestProcessor.java`: `java -cp target/streams-1.0-SNAPSHOT-standalone.jar com.example.TestProcessor`

6) Run the `AvroTestProducer.java` to produce commands: `java -cp target/streams-1.0-SNAPSHOT-standalone.jar com.example.producers.AvroTestProducer`

7) Check if the data is replicated to postgres
- `psql -U postgres -h localhost -p 7999 -f test.sql`
- `psql -U postgres -h localhost -p 7999 -f test2.sql`