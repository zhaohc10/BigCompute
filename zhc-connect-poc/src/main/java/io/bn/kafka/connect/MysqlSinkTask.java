package io.bn.kafka.connect;

/**
 * Created by zhc on 7/12/17.
 */
import org.apache.kafka.clients.consumer.OffsetAndMetadata;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.connect.sink.SinkRecord;
import org.apache.kafka.connect.sink.SinkTask;
import org.apache.kafka.common.utils.AppInfoParser;
import org.apache.kafka.connect.sink.SinkTaskContext;

import java.util.Collection;
import java.util.Map;


/**
 * Created by zhc on 7/11/17.
 */
public class MysqlSinkTask extends SinkTask {

    /**
     * Initialise sink task
     * @param context context of the sink task
     */
    @Override
    public void initialize(SinkTaskContext context) {


    }//initialize()

    @Override
    public String version() {
        return AppInfoParser.getVersion();
    }

    @Override
    public void start(Map<String, String> map) {
        /*
        This should handle any configuration parsing and one-time setup of the task.
         */

    }

    @Override
    public void put(Collection<SinkRecord> records) {
        /*
        Put the records in the sink.
        Usually this should send the records to the sink asynchronously and immediately return.
         */

        for (SinkRecord record: records ){
            System.out.println("zhc hahaha" + record.value());
        }
    }


    @Override
    public void flush(Map<TopicPartition, OffsetAndMetadata> offsets){

    }


    @Override
    public void stop() {

    }



    /*
    The SinkTask use onPartitionsAssigned method to
        create writers for newly assigned partitions in case of partition re-assignment.

    The SinkTask use onPartitionsRevoked method to
        close writers and commit offsets for partitions that are longer assigned to the SinkTask.
        This method will be called before a rebalance operation starts and after the SinkTask stops fetching data.

     */


}