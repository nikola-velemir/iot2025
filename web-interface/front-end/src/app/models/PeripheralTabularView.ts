import {Signal} from '@angular/core';

export type PeripheralType = "Sensor" | "Actuator";

export interface PeripheralTabularView {
  name: string;
  type: string;
  peripheralType: PeripheralType;
  action?: {
    name: string,
    callback: () => void;
  };
  currentState: Signal<string>;
  grafanaUrl: string;
}
