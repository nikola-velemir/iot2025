package org.lukavelemir.backend.service.common;

import org.springframework.stereotype.Component;

import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

@Component
public class GlobalState {
    private final AtomicInteger personCount = new AtomicInteger(0);
    private final AtomicBoolean alarmArmed = new AtomicBoolean(false);
    private final AtomicBoolean alarmOn = new AtomicBoolean(false);

    private final AtomicReference<String> lastStatus = new AtomicReference<>("INIT");

    public int getPersonCount() { return personCount.get(); }
    public void incrementSensor() { personCount.incrementAndGet(); }

    public String getLastStatus() { return lastStatus.get(); }
    public void setLastStatus(String status) { lastStatus.set(status); }
}
