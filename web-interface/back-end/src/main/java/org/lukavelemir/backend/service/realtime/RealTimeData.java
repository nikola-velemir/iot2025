package org.lukavelemir.backend.service.realtime;

public record RealTimeData(
        boolean isAlarmOn,
        Pi1 pi1,
        Pi2 pi2,
        Pi3 pi3
) {
    public static RealTimeData empty() {
        return new RealTimeData(false, Pi1.empty(), Pi2.empty(), Pi3.empty());
    }
}

record Pi1(
        String ds1,
        String dpir1,
        String dus1,
        String webc,
        String dl,
        String dms,
        String db
) {
    public static Pi1 empty() {
        return new Pi1("", "", "", "", "", "", "");
    }
}

record Pi2(
        String dus2,
        String dpir2,
        String ds2,
        String four_sd,
        String btn,
        String dht3,
        String gyr
) {
    public static Pi2 empty() {
        return new Pi2("", "", "", "", "", "", "");
    }
}

record Pi3(
        String ir,
        String dht2,
        String brgb,
        String lcd,
        String dpir3,
        String dht1
) {
    public static Pi3 empty() {
        return new Pi3("", "", "", "", "", "");
    }
}