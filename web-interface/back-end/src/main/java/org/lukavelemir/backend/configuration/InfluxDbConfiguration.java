package org.lukavelemir.backend.configuration;

import com.influxdb.client.InfluxDBClient;
import com.influxdb.client.InfluxDBClientFactory;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.env.Environment;

@Configuration
public class InfluxDbConfiguration {
    private final String url;
    private final String token;
    private final String organization;
    private final String defaultBucket;

    public InfluxDbConfiguration(Environment env) {
        this.url = String.format("http://%s:%s", env.getProperty("influxdb.host"), env.getProperty("influxdb.port"));
        this.token = env.getProperty("influxdb.token");
        this.organization = env.getProperty("influxdb.organization");
        this.defaultBucket = env.getProperty("influxdb.bucket");
    }

    public InfluxDBClient createClient(String bucket) {
        String actualBucket = (bucket == null || bucket.isEmpty()) ? this.defaultBucket : bucket;
        return InfluxDBClientFactory.create(this.url, this.token.toCharArray(), this.organization, actualBucket);
    }
}
