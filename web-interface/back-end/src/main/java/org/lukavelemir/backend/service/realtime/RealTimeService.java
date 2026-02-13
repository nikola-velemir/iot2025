package org.lukavelemir.backend.service.realtime;

import lombok.RequiredArgsConstructor;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class RealTimeService {
    private final SimpMessagingTemplate messagingTemplate;

    @Scheduled(fixedRate = 3000)
    public void broadcastRealTimeData() {
        try {
            RealTimeData realTimeData = RealTimeData.empty();
            messagingTemplate.convertAndSend("/data/user", realTimeData);
        } catch (Exception e) {
            System.out.println("Error processing topic");
        }
    }
}
