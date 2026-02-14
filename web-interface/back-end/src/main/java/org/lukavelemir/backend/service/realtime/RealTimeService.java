package org.lukavelemir.backend.service.realtime;

import com.influxdb.client.InfluxDBClient;
import com.influxdb.query.FluxRecord;
import com.influxdb.query.FluxTable;
import org.lukavelemir.backend.configuration.InfluxDbConfiguration;
import org.lukavelemir.backend.service.common.GlobalState;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class RealTimeService {
    private final SimpMessagingTemplate messagingTemplate;
    private final GlobalState globalState;
    private final InfluxDBClient influxDbClient;

    public RealTimeService(
            InfluxDbConfiguration influxDbConfiguration,
            SimpMessagingTemplate messagingTemplate,
            GlobalState globalState
    ) {
        this.globalState = globalState;
        this.messagingTemplate = messagingTemplate;
        this.influxDbClient = influxDbConfiguration.createClient("iotBucket");
    }

    @Scheduled(fixedRate = 1000)
    public void broadcastRealTimeData() {
        try {
            RealTimeData realTimeData = fetchFullRealTimeState(globalState);

            messagingTemplate.convertAndSend("/data/user", realTimeData);
        } catch (Exception e) {
            System.out.println("Error processing topic");
        }
    }

    public RealTimeData fetchFullRealTimeState(GlobalState globalState) {
        String query = "from(bucket: \"iotBucket\") " +
                "|> range(start: -10m) " +
                "|> last()";

        List<FluxTable> tables = influxDbClient.getQueryApi().query(query);

        Map<String, String> sensorMap = new HashMap<>();

        for (FluxTable table : tables) {
            for (FluxRecord record : table.getRecords()) {
                String device = (String) record.getValueByKey("device_name");
                String sensorName = (String) record.getValueByKey("name");
                String fieldName = record.getField();

                if (device == null || sensorName == null) continue;

                String baseKey = device.toLowerCase() + "_" + sensorName.toLowerCase();

                String finalKey;
                if (fieldName.startsWith("value_")) {
                    String axis = fieldName.replace("value_", "");
                    finalKey = baseKey + "_" + axis;
                } else if (sensorName.toLowerCase().contains("dht")) {
                    finalKey = baseKey + "_" + record.getMeasurement().toLowerCase();
                } else {
                    finalKey = baseKey;
                }

                sensorMap.put(finalKey, String.valueOf(record.getValue()));
            }
        }

        return mapToRecord(sensorMap, globalState);
    }

    private RealTimeData mapToRecord(Map<String, String> m, GlobalState globalState) {
        return new RealTimeData(
                globalState.isAlarmOn(),
                new Pi1(
                        Boolean.parseBoolean(m.getOrDefault("pi1_ds1", "false")) ? "DOOR OPEN" : "DOOR CLOSED",
                        Boolean.parseBoolean(m.getOrDefault("pi1_dpir1", "false")) ? "MOTION DETECTED" : "NO MOTION",
                        String.format("Distance: %.2f meters", Double.parseDouble(m.getOrDefault("pi1_dus1", "0.0"))),
                        m.getOrDefault("pi1_webc", ""), // todo webcam
                        Boolean.parseBoolean(m.getOrDefault("pi1_dl", "false")) ? "ON" : "OFF",
                        String.format("Last key pressed: %s", m.getOrDefault("pi1_dms", "none")),
                        Boolean.parseBoolean(m.getOrDefault("pi1_db", "false")) ? "ON" : "OFF"
                ),
                new Pi2(
                        String.format("Distance: %.2f meters", Double.parseDouble(m.getOrDefault("pi2_dus2", "0.0"))),
                        Boolean.parseBoolean(m.getOrDefault("pi2_dpir2", "false")) ? "MOTION DETECTED" : "NO MOTION",
                        Boolean.parseBoolean(m.getOrDefault("pi2_ds2", "false")) ? "DOOR OPEN" : "DOOR CLOSED",
                        m.getOrDefault("pi2_four_sd", ""), // todo stopwatch
                        Boolean.parseBoolean(m.getOrDefault("pi2_btn", "false")) ? "PRESSED" : "NOT PRESSED",
                        String.format(
                            "Temperature: %.2fC, Humidity: %.1f%%",
                            Double.parseDouble(m.getOrDefault("pi2_dht3_temperature", "0.0")),
                            Double.parseDouble(m.getOrDefault("pi2_dht3_humidity", "0.0"))
                        ),
                        String.format(
                                "X: %.2f, Y: %.2f, Z: %.2f",
                                Double.parseDouble(m.getOrDefault("pi2_gyr_x", "0.0")),
                                Double.parseDouble(m.getOrDefault("pi2_gyr_y", "0.0")),
                                Double.parseDouble(m.getOrDefault("pi2_gyr_z", "0.0"))
                        )
                ),
                new Pi3(
                        String.format("Command: %s", m.getOrDefault("pi3_ir", "NONE")),
                        String.format(
                                "Temperature: %.2fC, Humidity: %.1f%%",
                                Double.parseDouble(m.getOrDefault("pi3_dht2_temperature", "0.0")),
                                Double.parseDouble(m.getOrDefault("pi3_dht2_humidity", "0.0"))
                        ),
                        Boolean.parseBoolean(m.getOrDefault("pi3_brgb", "false")) ? "ON" : "OFF",
                        String.format("Text: \"%s\"", m.getOrDefault("pi3_lcd", "")),
                        Boolean.parseBoolean(m.getOrDefault("pi3_dpir3", "false")) ? "MOTION DETECTED" : "NO MOTION",
                        String.format(
                                "Temperature: %.2fC, Humidity: %.1f%%",
                                Double.parseDouble(m.getOrDefault("pi3_dht1_temperature", "0.0")),
                                Double.parseDouble(m.getOrDefault("pi3_dht1_humidity", "0.0"))
                        )
                )
        );
    }
}
