package com.example.producers;

import com.example.TestProcessor;
import com.example.avro.Test;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerRecord;

import java.util.Properties;
import java.util.UUID;

public class AvroTestProducer {

    public static void main(String[] args) throws InterruptedException {
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("acks", "all");
        props.put("retries", 0);
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", "io.confluent.kafka.serializers.KafkaAvroSerializer");
        props.put("schema.registry.url", TestProcessor.SCHEMA_REGISTRY_URL);

        String topic = "test";
        int wait = 500;

        Producer<String, Test> producer = new KafkaProducer<>(props);

        while (true) {
            Test command = CommandGenerator.getNextTest();
            System.out.println("Generated event " + command.toString());

            ProducerRecord<String, Test> record = new ProducerRecord<>(topic, UUID.randomUUID().toString(), command);
            producer.send(record);
            Thread.sleep(wait);
        }
    }
}
