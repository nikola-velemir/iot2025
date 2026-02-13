package org.lukavelemir.backend.service.common;

import org.springframework.stereotype.Component;

import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

@Component
public class GlobalState {
    private final AtomicInteger personCount = new AtomicInteger(0);
    private final AtomicBoolean alarmArmed = new AtomicBoolean(false);
    private final AtomicBoolean alarmOn = new AtomicBoolean(false);

    public int getPersonCount() { return personCount.get(); }
    public void incrementPersonCount() { personCount.incrementAndGet(); }
    public void decrementPersonCount() { personCount.decrementAndGet(); }

    public boolean isAlarmOn() { return alarmOn.get(); }
    public void turnOffAlarm() { alarmOn.set(false); }
    public void turnOnAlarm() { alarmOn.set(true); }

    public boolean isAlarmArmed() { return alarmArmed.get(); }
    public void armAlarm() { alarmArmed.set(true); }
    public void disarmAlarm() { alarmArmed.set(false); }
}
