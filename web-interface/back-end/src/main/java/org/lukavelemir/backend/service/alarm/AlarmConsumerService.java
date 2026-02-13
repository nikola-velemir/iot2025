package org.lukavelemir.backend.service.alarm;

import lombok.RequiredArgsConstructor;
import org.lukavelemir.backend.service.common.GlobalState;
import org.springframework.integration.annotation.ServiceActivator;
import org.springframework.messaging.Message;
import org.springframework.stereotype.Service;

/// Updates the state of the alarm.

@RequiredArgsConstructor
@Service
public class AlarmConsumerService {
    private final GlobalState globalState;

    @ServiceActivator(inputChannel = "alarmConsumerChannel")
    public void consume(Message<String> message) {
        String payload = message.getPayload();
        System.out.println("Stored: " + payload);
    }

    private void updatePeopleInBuilding() {
        switch ("left") {
            case "left" -> System.out.println("LEFT");
            case "entered" -> System.out.println("ENTERED");
            default -> throw new RuntimeException("Incorrect type");
        }
    }

    private void activateAlarmIfArmed() {

    }

    private void armAlarm() {

    }
}
