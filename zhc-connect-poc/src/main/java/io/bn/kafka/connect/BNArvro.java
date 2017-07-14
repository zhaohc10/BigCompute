//package io.bn.kafka.connect;
//
///**
// * Created by zhc on 7/12/17.
// */
//import io.confluent.connect.avro.AvroConverter;
//import io.confluent.connect.avro.AvroConverter;
//import io.confluent.kafka.schemaregistry.client.SchemaRegistryClient;
//import io.confluent.kafka.serializers.KafkaAvroSerializer;
//
//import org.apache.kafka.connect.data.SchemaAndValue;
//
//
//
//import java.io.IOException;
//import java.nio.ByteBuffer;
//import java.util.ArrayList;
//import java.util.Collections;
//import java.util.HashMap;
//import java.util.List;
//import java.util.Map;
//
//public class BNArvro {
//
//
//
//
//    private void printGenericRecord(byte[] is, String topic) throws IOException {
//
//        Map<String, String> config = new HashMap<>();
//        config.put("schema.registry.url", "http://192.168.33.10:8081");
//        AvroConverter converter = new AvroConverter();
//        converter.configure(config, false);
//        SchemaAndValue schemaAndValue = converter.toConnectData(topic, is);
//        Object value = schemaAndValue.value();
//        System.out.println("value = " + new StructWrapper().asCsv((Struct) value));
////
////        Schema schema = reader.getSchema();
////        for (Object o : reader) {
////            GenericRecord record = (GenericRecord)o;
////            log(record);
////        }
//
//    }
//
//}