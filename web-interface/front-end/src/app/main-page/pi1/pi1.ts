import {Component, computed, inject} from '@angular/core';
import {PeripheralTable} from '../../peripheral-table/peripheral-table';
import {GlobalStateService} from '../../services/global-state-service';
import {PeripheralTabularView} from '../../models/PeripheralTabularView';
import {MatDialog} from '@angular/material/dialog';
import {CameraDialog} from '../../dialog/camera-dialog/camera-dialog';

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
    dialog = inject(MatDialog);

    peripherals: PeripheralTabularView[] = [
      {
        name: 'DS1', type: 'Door sensor', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi1.ds1),
        grafanaUrl: "http://localhost:3000/d-solo/ddaacbac-473a-4982-a690-9c22cd365de1/pi1?orgId=1&timezone=browser&refresh=10s&panelId=panel-2&__feature.dashboardSceneSolo=true"
      },
      {
        name: 'DPIR1', type: 'Motion sensor', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi1.dpir1),
        grafanaUrl: "http://localhost:3000/d-solo/ddaacbac-473a-4982-a690-9c22cd365de1/pi1?orgId=1&timezone=browser&refresh=10s&panelId=panel-4&__feature.dashboardSceneSolo=true"
      },
      {
        name: 'DUS1', type: 'Ultrasonic sensor', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi1.dus1),
        grafanaUrl: "http://localhost:3000/d-solo/ddaacbac-473a-4982-a690-9c22cd365de1/pi1?orgId=1&timezone=browser&refresh=10s&panelId=panel-1&__feature.dashboardSceneSolo=true"
      },
      {
        name: 'WEBC', type: 'Web camera', peripheralType: 'Sensor',
        action: { 'name': "View camera", callback: () => this.openCamera() },
        currentState: computed(() => this.globalState.data().pi1.webc),
        grafanaUrl: ""
      },
      {
        name: 'DL', type: 'LED', peripheralType: 'Actuator',
        currentState: computed(() => this.globalState.data().pi1.dl),
        grafanaUrl: "http://localhost:3000/d-solo/ddaacbac-473a-4982-a690-9c22cd365de1/pi1?orgId=1&timezone=browser&refresh=10s&panelId=panel-3&__feature.dashboardSceneSolo=true"
      },
      {
        name: 'DMS', type: 'Keypad', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi1.dms),
        grafanaUrl: "http://localhost:3000/d-solo/ddaacbac-473a-4982-a690-9c22cd365de1/pi1?orgId=1&timezone=browser&refresh=10s&panelId=panel-6&__feature.dashboardSceneSolo=true"
      },
      {
        name: 'DB', type: 'Buzzer', peripheralType: 'Actuator',
        currentState: computed(() => this.globalState.data().pi1.db),
        grafanaUrl: "http://localhost:3000/d-solo/ddaacbac-473a-4982-a690-9c22cd365de1/pi1?orgId=1&timezone=browser&refresh=10s&panelId=panel-5&__feature.dashboardSceneSolo=true"
      },
    ];

  openCamera = async () => {
    this.dialog.open(CameraDialog, {
      height: '300px',
    });
  }
}
