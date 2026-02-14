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

    @Scheduled(fixedRate = 3000)
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
                Object value = record.getValue();

                if (device != null && sensorName != null) {
                    sensorMap.put(device.toLowerCase() + "_" + sensorName.toLowerCase(), String.valueOf(value));
                }
            }
        }

        return mapToRecord(sensorMap, globalState);
    }

    private RealTimeData mapToRecord(Map<String, String> m, GlobalState globalState) {
        return new RealTimeData(
                globalState.isAlarmOn(),
                new Pi1(
                        m.getOrDefault("pi1_ds1", ""), m.getOrDefault("pi1_dpir1", ""),
                        m.getOrDefault("pi1_dus1", ""), m.getOrDefault("pi1_webc", ""),
                        m.getOrDefault("pi1_dl", ""), m.getOrDefault("pi1_dms", ""),
                        m.getOrDefault("pi1_db", "")
                ),
                new Pi2(
                        m.getOrDefault("pi2_dus2", ""), m.getOrDefault("pi2_dpir2", ""),
                        m.getOrDefault("pi2_ds2", ""), m.getOrDefault("pi2_four_sd", ""),
                        m.getOrDefault("pi2_btn", ""), m.getOrDefault("pi2_dht3", ""),
                        m.getOrDefault("pi2_gyr", "")
                ),
                new Pi3(
                        m.getOrDefault("pi3_ir", ""), m.getOrDefault("pi3_dht2", ""),
                        m.getOrDefault("pi3_brgb", ""), m.getOrDefault("pi3_lcd", ""),
                        m.getOrDefault("pi3_dpir3", ""), m.getOrDefault("pi3_dht1", "")
                )
        );
    }
}
