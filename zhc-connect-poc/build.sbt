name := "zhc-java"

version := "1.0"

scalaVersion := "2.11.8"

lazy val versions = Map(
  "kafka" -> "0.10.0.0",
  "confluent" -> "3.0.0",
  "scalaTest" -> "3.0.0"
)
libraryDependencies ++= Seq(
  "org.apache.kafka" %% "kafka" % versions("kafka"),
  "org.apache.kafka" % "connect-api" % versions("kafka"),
  "io.confluent" % "common-config" % versions("confluent"),
  "io.confluent" % "kafka-avro-serializer" % versions("confluent"),
//  "io.confluent" % "kafka-connect-avro-converter" % "3.1.0-SNAPSHOT",
  "io.confluent" % "kafka-schema-registry-client" % versions("confluent")

)

        