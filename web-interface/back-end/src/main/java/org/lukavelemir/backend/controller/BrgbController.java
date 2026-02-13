package org.lukavelemir.backend.controller;

import lombok.RequiredArgsConstructor;
import org.lukavelemir.backend.controller.dto.NewBrgbColor;
import org.lukavelemir.backend.service.BRGB.BRGBProducerService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/brgb")
@RequiredArgsConstructor
public class BrgbController {
    private final BRGBProducerService brgbProducerService;

    @PostMapping("/set")
    private ResponseEntity<?> setBrgbLight(@RequestBody NewBrgbColor newBrgbColor) {
        brgbProducerService.sendBrgbLightUpdate(newBrgbColor.color());

        return ResponseEntity.ok().build();
    }
}
