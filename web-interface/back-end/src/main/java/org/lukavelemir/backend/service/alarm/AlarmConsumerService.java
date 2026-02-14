package org.lukavelemir.backend.service.alarm;

import lombok.RequiredArgsConstructor;
import org.lukavelemir.backend.service.common.GlobalState;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.integration.annotation.ServiceActivator;
import org.springframework.messaging.Message;
import org.springframework.stereotype.Service;
import tools.jackson.databind.JsonNode;
import tools.jackson.databind.ObjectMapper;

import java.util.concurrent.locks.ReentrantLock;

@RequiredArgsConstructor
@Service
public class AlarmConsumerService {
    private final GlobalState globalState;
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final AlarmProducerService alarmProducerService;
    private final ReentrantLock armingLock = new ReentrantLock();

    @Value("${app.alarm.pin}")
    private String alarmPin;

    @ServiceActivator(inputChannel = "alarmConsumerChannel")
    public void consume(Message<String> message) {
        try {
            String payload = message.getPayload();
            JsonNode json = objectMapper.readTree(payload);
            String type = json.path("type").stringValue();

            switch (type) {
                case "try_arm" -> armAlarm(json.path("pin").stringValue());
                case "person_event" -> updatePeopleInBuilding(json.get("person_event").stringValue());
                case "motion" -> motionDetectedPir();
                case "gyro" -> motionDetectedGyro();
                case "open_too_long" -> doorButtonNotPressedForMoreThan5Seconds();
                default -> System.out.println("Unknown message type received: " + type);
            }

        } catch (Exception e) {
            System.err.println("Failed to parse MQTT JSON: " + e.getMessage());
        }
    }

    private void updatePeopleInBuilding(String event) {
        switch (event) {
            case "left" -> globalState.decrementPersonCount();
            case "entered" -> globalState.incrementPersonCount();
            default -> throw new RuntimeException("Incorrect type");
        }
    }

    private void armAlarm(String pin) {
        if (!armingLock.tryLock()) {
            System.out.println("REQUEST REJECTED: Arming process already in progress.");
            return;
        }

        try {
            if (pin.equals(alarmPin)) {
                if (globalState.isAlarmArmed()) {
                    System.out.println("ALARM DISARMED: " + pin);
                    globalState.turnOffAlarm();
                    globalState.disarmAlarm();
                    alarmProducerService.sendAlarmDeactivationSignal();
                } else {
                    System.out.println("STARTING 10s ARM COUNTDOWN");
                    Thread.sleep(10000);
                    globalState.armAlarm();
                    System.out.println("ALARM ARMED: " + pin);
                }
            } else {
                globalState.turnOnAlarm();
                globalState.armAlarm();
                alarmProducerService.sendAlarmActivationSignal();
                System.out.println("PIN NOT CORRECT, TURNING ON ALARM: " + pin);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            armingLock.unlock();
        }
    }

    private void motionDetectedPir() {
        System.out.println("MOTION DETECTED BY PIR");

        if (globalState.getPersonCount() == 0) {
            activateAlarmIfArmed();
        }
    }

    private void motionDetectedGyro() {
        System.out.println("MOTION DETECTED BY GYRO");
        activateAlarmIfArmed();
    }

    private void doorButtonNotPressedForMoreThan5Seconds() {
        System.out.println("DOOR OPENED FOR MOE THAN 5 SECONDS");
        activateAlarmIfArmed();
    }

    private void activateAlarmIfArmed() {
        if (globalState.isAlarmArmed()) {
            globalState.turnOnAlarm();
            alarmProducerService.sendAlarmActivationSignal();
        }
    }
}
