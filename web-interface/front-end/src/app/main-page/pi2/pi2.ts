import {Component, computed, inject} from '@angular/core';
import {PeripheralTable} from '../../peripheral-table/peripheral-table';
import {MatDialog, MatDialogRef} from '@angular/material/dialog';
import {StopwatchDialog} from '../../dialog/stopwatch-dialog/stopwatch-dialog';
import {firstValueFrom} from 'rxjs';
import {StopwatchService} from '../../services/stopwatch-service';
import {GlobalStateService} from '../../services/global-state-service';
import {PeripheralTabularView} from '../../models/PeripheralTabularView';

@Component({
  selector: 'app-pi2',
  imports: [
    PeripheralTable
  ],
  templateUrl: './pi2.html',
  styleUrl: './pi2.scss',
})
export class Pi2 {
    dialog = inject(MatDialog);
    stopWatchService = inject(StopwatchService);
    globalState = inject(GlobalStateService);

    peripherals: PeripheralTabularView[] = [
      {
        name: 'DUS2', type: 'Ultrasonic sensor', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi2.dus2),
        grafanaUrl: "http://localhost:3000/d-solo/ddaacbac-473a-4982-a690-9c22cd365de2/pi2?orgId=1&timezone=browser&refresh=10s&panelId=panel-6&__feature.dashboardSceneSolo=true"
      },
      {
        name: 'DPIR2', type: 'Motion sensor', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi2.dpir2),
        grafanaUrl: "http://localhost:3000/d-solo/ddaacbac-473a-4982-a690-9c22cd365de2/pi2?orgId=1&timezone=browser&refresh=10s&panelId=panel-5&__feature.dashboardSceneSolo=true"
      },
      {
        name: 'DS2', type: 'Door sensor', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi2.ds2),
        grafanaUrl: "http://localhost:3000/d-solo/ddaacbac-473a-4982-a690-9c22cd365de2/pi2?orgId=1&timezone=browser&refresh=10s&panelId=panel-4&__feature.dashboardSceneSolo=true"
      },
      {
        name: '4SD', type: '4 segment display', peripheralType: 'Actuator',
        action: { 'name': "Initialize stopwatch", callback: () => this.openStopwatchSettingsDialog() },
        currentState: computed(() => this.globalState.data().pi2.four_sd),
        grafanaUrl: "http://localhost:3000/d-solo/ddaacbac-473a-4982-a690-9c22cd365de2/pi2?orgId=1&timezone=browser&refresh=10s&panelId=panel-10&__feature.dashboardSceneSolo=true"
      },
      {
        name: 'BTN', type: 'Button', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi2.btn),
        grafanaUrl: "http://localhost:3000/d-solo/ddaacbac-473a-4982-a690-9c22cd365de2/pi2?orgId=1&timezone=browser&refresh=10s&panelId=panel-9&__feature.dashboardSceneSolo=true"
      },
      {
        name: 'DHT3', type: 'Temperature sensor', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi2.dht3),
        grafanaUrl: "http://localhost:3000/d-solo/ddaacbac-473a-4982-a690-9c22cd365de2/pi2?orgId=1&timezone=browser&refresh=10s&panelId=panel-7&__feature.dashboardSceneSolo=true"
      },
      {
        name: 'GYR', type: 'Gyroscope', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi2.gyr),
        grafanaUrl: "http://localhost:3000/d-solo/ddaacbac-473a-4982-a690-9c22cd365de2/pi2?orgId=1&timezone=browser&refresh=10s&panelId=panel-8&__feature.dashboardSceneSolo=true"
      },
    ];

    openStopwatchSettingsDialog = async () => {
        const dialogRef: MatDialogRef<StopwatchDialog, { startingDuration: number, increaseDuration: number } | null | undefined> = this.dialog.open(StopwatchDialog, {
          height: '300px',
        });

        const result = await firstValueFrom(dialogRef.afterClosed());

        if (result) {
          try {
            await firstValueFrom(this.stopWatchService.initializeStopwatch(result?.startingDuration!, result?.increaseDuration!));
          } catch (e) {
            console.error("Error initializing stopwatch")
          }
        }
    }
}
