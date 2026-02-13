package org.lukavelemir.backend.controller;

import lombok.RequiredArgsConstructor;
import org.lukavelemir.backend.controller.dto.StopwatchInitialization;
import org.lukavelemir.backend.service.stopwatch.StopwatchProducerService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/stopwatch")
@RequiredArgsConstructor
public class StopwatchController {
    private final StopwatchProducerService stopwatchProducerService;

    @PostMapping("/initialize")
    private ResponseEntity<?> initialize(@RequestBody StopwatchInitialization stopwatchInitialization) {
        stopwatchProducerService.sendStopwatchStart(stopwatchInitialization.totalMinutes(), stopwatchInitialization.rampUpSeconds());

        return ResponseEntity.ok().build();
    }
}
