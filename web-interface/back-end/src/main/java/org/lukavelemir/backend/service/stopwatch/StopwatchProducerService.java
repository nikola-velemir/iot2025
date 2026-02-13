package org.lukavelemir.backend.service.stopwatch;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.integration.mqtt.support.MqttHeaders;
import org.springframework.integration.support.MessageBuilder;
import org.springframework.messaging.MessageHandler;
import org.springframework.stereotype.Service;

@Service
public class StopwatchProducerService {
    private final MessageHandler stopwatchProducerChannel;

    public StopwatchProducerService(@Qualifier("stopwatchProducer") MessageHandler handler) {
        this.stopwatchProducerChannel = handler;
    }

    public void sendStopwatchStart(int totalMinutes, int rampUpSeconds) {
        stopwatchProducerChannel.handleMessage(
                MessageBuilder.withPayload(String.format("STOPWATCH_STARTED:%d,%d", totalMinutes, rampUpSeconds))
                        .setHeader(MqttHeaders.TOPIC, "back_receive/stopwatch")
                        .build()
        );
    }
}