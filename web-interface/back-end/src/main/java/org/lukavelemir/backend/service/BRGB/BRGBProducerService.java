package org.lukavelemir.backend.service.BRGB;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.integration.mqtt.support.MqttHeaders;
import org.springframework.integration.support.MessageBuilder;
import org.springframework.messaging.MessageHandler;
import org.springframework.stereotype.Service;

@Service
public class BRGBProducerService {
    private final MessageHandler bgrbProducerChannel;

    public BRGBProducerService(@Qualifier("brgbProducer") MessageHandler handler) {
        this.bgrbProducerChannel = handler;
    }

    public void sendBrgbLightUpdate(String color) {
        bgrbProducerChannel.handleMessage(
                MessageBuilder.withPayload(String.format("BRGB_NEW_LIGHT:%s", color))
                        .setHeader(MqttHeaders.TOPIC, "back_receive/brgb")
                        .build()
        );
    }
}
