import { Component } from '@angular/core';
import {PeripheralTable, TableRow} from '../../peripheral-table/peripheral-table';

@Component({
  selector: 'app-pi1',
  imports: [
    PeripheralTable,
  ],
  templateUrl: './pi1.html',
  styleUrl: './pi1.scss',
})
export class Pi1 {
    peripherals: TableRow[] = [
      {
        name: 'DS1', type: 'Door sensor', peripheralType: 'Sensor',
        currentState: "TEST_STATE", grafanaUrl: ""
      },
      {
        name: 'DPIR1', type: 'Motion sensor', peripheralType: 'Sensor',
        currentState: "TEST_STATE", grafanaUrl: ""
      },
      {
        name: 'DUS1', type: 'Ultrasonic sensor', peripheralType: 'Sensor',
        currentState: "TEST_STATE", grafanaUrl: ""
      },
      {
        name: 'WEBC', type: 'Web camera', peripheralType: 'Sensor',
        currentState: "TEST_STATE", grafanaUrl: ""
      },
      {
        name: 'DL', type: 'LED', peripheralType: 'Actuator',
        currentState: "TEST_STATE", grafanaUrl: ""
      },
      {
        name: 'DMS', type: 'Keypad', peripheralType: 'Sensor',
        currentState: "TEST_STATE", grafanaUrl: ""
      },
      {
        name: 'DB', type: 'Buzzer', peripheralType: 'Actuator',
        currentState: "TEST_STATE", grafanaUrl: ""
      },
    ];
}
