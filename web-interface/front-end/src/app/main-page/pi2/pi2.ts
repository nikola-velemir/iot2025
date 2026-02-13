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
        grafanaUrl: ""
      },
      {
        name: 'DPIR2', type: 'Motion sensor', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi2.dpir2),
        grafanaUrl: ""
      },
      {
        name: 'DS2', type: 'Door sensor', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi2.ds2),
        grafanaUrl: ""
      },
      {
        name: '4SD', type: '4 segment display', peripheralType: 'Actuator',
        action: { 'name': "Stopwatch settings", callback: () => this.openStopwatchSettingsDialog() },
        currentState: computed(() => this.globalState.data().pi2.four_sd),
        grafanaUrl: ""
      },
      {
        name: 'BTN', type: 'Button', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi2.btn),
        grafanaUrl: ""
      },
      {
        name: 'DHT3', type: 'Temperature sensor', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi2.dht3),
        grafanaUrl: ""
      },
      {
        name: 'GYR', type: 'Gyroscope', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi2.gyr),
        grafanaUrl: ""
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
