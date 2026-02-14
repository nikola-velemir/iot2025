export interface RealTimeData {
  isAlarmOn: boolean;
  pi1: Pi1;
  pi2: Pi2;
  pi3: Pi3;
}

export interface Pi1 {
  ds1: string;
  dpir1: string;
  dus1: string;
  webc: string;
  dl: string;
  dms: string;
  db: string;
}

export interface Pi2 {
  dus2: string;
  dpir2: string;
  ds2: string;
  four_sd: string;
  btn: string;
  dht3: string;
  gyr: string;
}

export interface Pi3 {
  ir: string;
  dht2: string;
  brgb: string;
  lcd: string;
  dpir3: string;
  dht1: string;
}

export const EMPTY_REAL_TIME_DATA: RealTimeData = {
  isAlarmOn: false,
  pi1: {
    ds1: '',
    dpir1: '',
    dus1: '',
    webc: '',
    dl: '',
    dms: '',
    db: ''
  },
  pi2: {
    dus2: '',
    dpir2: '',
    ds2: '',
    four_sd: '',
    btn: '',
    dht3: '',
    gyr: ''
  },
  pi3: {
    ir: '',
    dht2: '',
    brgb: '',
    lcd: '',
    dpir3: '',
    dht1: ''
  }
};
