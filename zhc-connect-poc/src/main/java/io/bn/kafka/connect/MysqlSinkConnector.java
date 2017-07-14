package io.bn.kafka.connect;

/**
 * Created by zhc on 7/12/17.
 */
import org.apache.kafka.common.config.ConfigDef;
import org.apache.kafka.common.utils.AppInfoParser;
import org.apache.kafka.connect.sink.SinkConnector;
import org.apache.kafka.connect.connector.Task;

import org.apache.kafka.connect.errors.ConnectException;


import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MysqlSinkConnector extends SinkConnector {

    public static final String HOST_CONFIG = "host";
    public static final String USER_CONFIG = "user";
    public static final String PASSWORD_CONFIG = "password";
    public static final String PORT_CONFIG = "port";

    private String host;
    private String user;
    private String password;
    private String port;

    @Override
    public ConfigDef config() {
        return null;
    }
    @Override
    public void start(Map<String,String> props){
        host =props.get(HOST_CONFIG);
        user = props.get(USER_CONFIG);
        password = props.get(PASSWORD_CONFIG);
        port = props.get(PORT_CONFIG);

        if (host == null || host.isEmpty()) {
            throw new ConnectException("mysql config must include host settings");
        }
    }

    @Override
    public Class<? extends Task> taskClass(){
        return MysqlSinkTask.class;
    }

    @Override
    public List<Map<String, String>> taskConfigs(int maxTasks){
        ArrayList<Map<String,String>> configs = new ArrayList<>();
        Map<String,String> config = new HashMap<>();
//        config.put("user",user);
//        config.put("password", password);
        config.put("host", host);
//        config.put("port", port);
        for (int i=0; i<maxTasks;i++){
            configs.add(config);
        }
        return configs;

    }

    @Override
    public void stop(){

    }

    @Override
    public String version(){
        return AppInfoParser.getVersion();
    }
}
