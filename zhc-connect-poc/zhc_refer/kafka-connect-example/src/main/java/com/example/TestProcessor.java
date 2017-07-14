package com.example;

import com.example.avro.Test;
import com.example.serializers.SpecificAvroSerde;
import io.confluent.kafka.schemaregistry.client.CachedSchemaRegistryClient;
import io.confluent.kafka.serializers.AbstractKafkaAvroSerDeConfig;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.KeyValue;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.KStreamBuilder;

import java.util.*;

public class TestProcessor {

    public static final String SCHEMA_REGISTRY_URL = "http://localhost:8081";

    public static void main(final String[] args) throws Exception {
        final Properties streamsConfiguration = new Properties();
        streamsConfiguration.put(StreamsConfig.APPLICATION_ID_CONFIG, "app");
        streamsConfiguration.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        streamsConfiguration.put(StreamsConfig.ZOOKEEPER_CONNECT_CONFIG, "localhost:2181");
        streamsConfiguration.put(AbstractKafkaAvroSerDeConfig.SCHEMA_REGISTRY_URL_CONFIG, SCHEMA_REGISTRY_URL);
        streamsConfiguration.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "latest");

        // setup
        final CachedSchemaRegistryClient schemaRegistry = new CachedSchemaRegistryClient(SCHEMA_REGISTRY_URL, 100);
        final Map<String, String> serdeProps = Collections.singletonMap("schema.registry.url", SCHEMA_REGISTRY_URL);

        final SpecificAvroSerde<Test> testSpecificAvroSerde = new SpecificAvroSerde<>(schemaRegistry, serdeProps);
        testSpecificAvroSerde.configure(serdeProps, false);

        // stream builder
        final KStreamBuilder builder = new KStreamBuilder();
        final KStream<String, Test> tests = builder.stream(Serdes.String(), testSpecificAvroSerde, "test");

        tests.map((id, command) -> {
            System.out.println("test id=" + id + " command=" + command);
            command.setId(9);

            return KeyValue.pair(UUID.randomUUID().toString(), command);
        })
            .to(Serdes.String(), testSpecificAvroSerde, "test2");

        System.out.println("starting stream...");

        // run it
        final KafkaStreams streams = new KafkaStreams(builder, streamsConfiguration);
        streams.start();

        // gracefully close Kafka Streams
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            try {
                streams.close();
            } catch (Exception e) {
                System.out.println(e);
            }
        }));
    }
}
