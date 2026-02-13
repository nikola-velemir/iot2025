package org.lukavelemir.backend.service.alarm;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.integration.mqtt.support.MqttHeaders;
import org.springframework.integration.support.MessageBuilder;
import org.springframework.messaging.MessageHandler;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

@Service
public class AlarmProducerService {
    private final MessageHandler alarmProducerChannel;

    public AlarmProducerService(@Qualifier("alarmProducer") MessageHandler handler) {
        this.alarmProducerChannel = handler;
    }

//    @Scheduled(fixedDelay = 3000)
//    public void publish() {
//        sendAlarmDeactivationSignal(); // todo remove, used for testing
//    }

    public void sendAlarmActivationSignal() {
        alarmProducerChannel.handleMessage(
                MessageBuilder.withPayload("ACTIVATE_ALARM:")
                    .setHeader(MqttHeaders.TOPIC, "back_receive/alarm")
                    .build()
        );
    }

    public void sendAlarmDeactivationSignal() {
        alarmProducerChannel.handleMessage(
                MessageBuilder.withPayload("DEACTIVATE_ALARM:")
                        .setHeader(MqttHeaders.TOPIC, "back_receive/alarm")
                        .build()
        );
    }
}
