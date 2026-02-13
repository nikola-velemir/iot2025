package org.lukavelemir.backend.configuration;

import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.integration.annotation.ServiceActivator;
import org.springframework.integration.channel.DirectChannel;
import org.springframework.integration.config.EnableIntegration;
import org.springframework.integration.core.MessageProducer;
import org.springframework.integration.mqtt.core.DefaultMqttPahoClientFactory;
import org.springframework.integration.mqtt.core.MqttPahoClientFactory;
import org.springframework.integration.mqtt.inbound.MqttPahoMessageDrivenChannelAdapter;
import org.springframework.integration.mqtt.outbound.MqttPahoMessageHandler;
import org.springframework.messaging.MessageChannel;
import org.springframework.messaging.MessageHandler;

@Configuration
@EnableIntegration
public class MqttConfig {
    @Bean
    public MqttPahoClientFactory mqttClientFactory() {
        DefaultMqttPahoClientFactory factory = new DefaultMqttPahoClientFactory();
        MqttConnectOptions options = new MqttConnectOptions();
        String BROKER_URL = "tcp://localhost:1883";
        options.setServerURIs(new String[] {BROKER_URL});
        options.setCleanSession(true);
        factory.setConnectionOptions(options);
        return factory;
    }

    // Channels for Alarm
    @Bean
    public MessageChannel alarmProducerChannel() { return new DirectChannel(); }

    @Bean(name = "alarmConsumerChannel")
    public MessageChannel alarmConsumerChannel() { return new DirectChannel(); }

    // Channels for BRGB
    @Bean
    public MessageChannel brgbProducerChannel() { return new DirectChannel(); }

    @Bean(name = "bgrbConsumerChannel")
    public MessageChannel brgbConsumerChannel() { return new DirectChannel(); }

    // Consumers
    @Bean
    public MessageProducer alarmConsumerAdapter(MqttPahoClientFactory factory) {
        MqttPahoMessageDrivenChannelAdapter adapter =
                new MqttPahoMessageDrivenChannelAdapter("alarm-sub", factory, "back_send/alarm");
        adapter.setOutputChannel(alarmConsumerChannel());
        return adapter;
    }

    @Bean
    public MessageProducer brgbConsumerAdapter(MqttPahoClientFactory factory) {
        MqttPahoMessageDrivenChannelAdapter adapter =
                new MqttPahoMessageDrivenChannelAdapter("brgb-sub", factory, "home/power/#");
        adapter.setOutputChannel(brgbConsumerChannel());
        return adapter;
    }

    // Producers
    @Bean(name = "alarmProducer")
    @ServiceActivator(inputChannel = "alarmProducerChannel")
    public MessageHandler alarmProducer(MqttPahoClientFactory factory) {
        return new MqttPahoMessageHandler("alarm-pub", factory);
    }

    @Bean(name = "brgbProducer")
    @ServiceActivator(inputChannel = "brgbProducerChannel")
    public MessageHandler brgbProducer(MqttPahoClientFactory factory) {
        return new MqttPahoMessageHandler("brgb-pub", factory);
    }
}