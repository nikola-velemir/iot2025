import {Component, computed, inject} from '@angular/core';
import {PeripheralTable} from '../../peripheral-table/peripheral-table';
import {GlobalStateService} from '../../services/global-state-service';
import {PeripheralTabularView} from '../../models/PeripheralTabularView';

@Component({
  selector: 'app-pi1',
  imports: [
    PeripheralTable,
  ],
  templateUrl: './pi1.html',
  styleUrl: './pi1.scss',
})
export class Pi1 {
    globalState = inject(GlobalStateService);

    peripherals: PeripheralTabularView[] = [
      {
        name: 'DS1', type: 'Door sensor', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi1.ds1),
        grafanaUrl: ""
      },
      {
        name: 'DPIR1', type: 'Motion sensor', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi1.dpir1),
        grafanaUrl: ""
      },
      {
        name: 'DUS1', type: 'Ultrasonic sensor', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi1.dus1),
        grafanaUrl: "http://localhost:3000/d-solo/ddaacbac-473a-4982-a690-9c22cd365de1/pi1?orgId=1&timezone=browser&refresh=10s&panelId=panel-1&__feature.dashboardSceneSolo=true"
      },
      {
        name: 'WEBC', type: 'Web camera', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi1.webc),
        grafanaUrl: ""
      },
      {
        name: 'DL', type: 'LED', peripheralType: 'Actuator',
        currentState: computed(() => this.globalState.data().pi1.dl),
        grafanaUrl: ""
      },
      {
        name: 'DMS', type: 'Keypad', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi1.dms),
        grafanaUrl: ""
      },
      {
        name: 'DB', type: 'Buzzer', peripheralType: 'Actuator',
        currentState: computed(() => this.globalState.data().pi1.db),
        grafanaUrl: ""
      },
    ];
}
