package org.lukavelemir.backend.service.alarm;

import lombok.RequiredArgsConstructor;
import org.lukavelemir.backend.service.common.GlobalState;
import org.springframework.integration.annotation.ServiceActivator;
import org.springframework.messaging.Message;
import org.springframework.messaging.simp.user.SimpUser;
import org.springframework.stereotype.Service;
import tools.jackson.databind.JsonNode;
import tools.jackson.databind.ObjectMapper;

/// Updates the state of the alarm.

@RequiredArgsConstructor
@Service
public class AlarmConsumerService {
    private final GlobalState globalState;
    private final ObjectMapper objectMapper = new ObjectMapper();

    @ServiceActivator(inputChannel = "alarmConsumerChannel")
    public void consume(Message<String> message) {
        try {
            String payload = message.getPayload();
            JsonNode json = objectMapper.readTree(payload);
            String type = json.path("type").stringValue();

            switch (type) {
                case "try_arm" -> armAlarm(json.path("pin").stringValue());
                case "person_event" -> updatePeopleInBuilding(json.get("person_event").stringValue());
                case "motion" -> motionDetected("motion sensor");
                case "gyro" -> motionDetected("gyro");
                default -> System.out.println("Unknown message type received: " + type);
            }

        } catch (Exception e) {
            System.err.println("Failed to parse MQTT JSON: " + e.getMessage());
        }
    }

    private void updatePeopleInBuilding(String event) {
        switch (event) {
            case "left" -> System.out.println("PERSON LEFT");
            case "entered" -> System.out.println("PERSON ENTERED");
            default -> throw new RuntimeException("Incorrect type");
        }
    }

    private void armAlarm(String pin) {
        System.out.println("ALARM TRIED TO BE ARMED WITH PIN: " + pin);
    }

    private void motionDetected(String type) {
        System.out.println("MOTION DETECTED BY " + type);
    }

    private void doorButtonNotPressedForMoreThan5Seconds() {
        System.out.println("DOOR OPENED FOR MOE THAN 5 SECONDS");
    }

    private void activateAlarmIfArmed() {

    }
}
