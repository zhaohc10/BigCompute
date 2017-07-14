package com.example.producers;

import com.example.avro.Test;

import java.util.Random;

public class CommandGenerator {

    private static Random r = new Random();

    public static Test getNextTest() {
        return Test.newBuilder()
            .setId(4)
            .setPrice(1)
            .setProduct("bar")
            .setQuantity(3)
            .build();
    }
}
