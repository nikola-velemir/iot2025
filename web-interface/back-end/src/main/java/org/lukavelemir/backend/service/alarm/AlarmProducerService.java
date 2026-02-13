package org.lukavelemir.backend.service.alarm;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.integration.mqtt.support.MqttHeaders;
import org.springframework.integration.support.MessageBuilder;
import org.springframework.messaging.MessageHandler;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

/// Sends the required signals to all devices when an alarm happens.

@Service
public class AlarmProducerService {
    private final MessageHandler alarmProducerChannel;

    public AlarmProducerService(@Qualifier("alarmProducer") MessageHandler handler) {
        this.alarmProducerChannel = handler;
    }

    @Scheduled(fixedDelay = 1000)
    public void publish() {
        alarmProducerChannel.handleMessage(MessageBuilder.withPayload("VELEMIRE VOLIM TE")
                .setHeader(MqttHeaders.TOPIC, "back_receive")
                .build());
    }
}
