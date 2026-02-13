package org.lukavelemir.backend.controller;

import lombok.RequiredArgsConstructor;
import org.lukavelemir.backend.service.alarm.AlarmProducerService;
import org.lukavelemir.backend.service.common.GlobalState;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/alarm")
@RequiredArgsConstructor
public class AlarmController {
    private final AlarmProducerService alarmProducerService;
    private final GlobalState globalState;

    @PostMapping("/off")
    private ResponseEntity<?> turnAlarmOff() {
        globalState.turnOffAlarm();
        alarmProducerService.sendAlarmDeactivationSignal();

        return ResponseEntity.ok().build();
    }
}
