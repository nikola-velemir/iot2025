import {Component, computed, inject} from '@angular/core';
import {PeripheralTable} from "../../peripheral-table/peripheral-table";
import {MatDialog, MatDialogRef} from '@angular/material/dialog';
import {firstValueFrom} from 'rxjs';
import {LightColorDialog} from '../../dialog/light-color-dialog/light-color-dialog';
import {BrgbService} from '../../services/brgb-service';
import {GlobalStateService} from '../../services/global-state-service';
import {PeripheralTabularView} from '../../models/PeripheralTabularView';

@Component({
  selector: 'app-pi3',
    imports: [
        PeripheralTable
    ],
  templateUrl: './pi3.html',
  styleUrl: './pi3.scss',
})
export class Pi3 {
    dialog = inject(MatDialog);
    brgbService = inject(BrgbService);
    globalState = inject(GlobalStateService);

    peripherals: PeripheralTabularView[] = [
      {
        name: 'IR', type: 'Infrared sensor', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi3.ir),
        grafanaUrl: ""
      },
      {
        name: 'DHT2', type: 'Temperature sensor', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi3.dht2),
        grafanaUrl: ""
      },
      {
        name: 'BGRB', type: 'Colored LED', peripheralType: 'Actuator',
        action: { 'name': "Set light color", callback: () => this.setColorOfBrgb() },
        currentState: computed(() => this.globalState.data().pi3.brgb),
        grafanaUrl: ""
      },
      {
        name: 'LCD', type: 'LCD display', peripheralType: 'Actuator',
        currentState: computed(() => this.globalState.data().pi3.lcd),
        grafanaUrl: ""
      },
      {
        name: 'DPIR3', type: 'Motion sensor', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi3.dpir3),
        grafanaUrl: ""
      },
      {
        name: 'DHT1', type: 'Temperature sensor', peripheralType: 'Sensor',
        currentState: computed(() => this.globalState.data().pi3.dht1),
        grafanaUrl: ""
      },
    ];

    setColorOfBrgb = async () => {
      const dialogRef: MatDialogRef<LightColorDialog, string | null | undefined> = this.dialog.open(LightColorDialog, {
        height: '250px',
      });

      const result = await firstValueFrom(dialogRef.afterClosed());

      if (result) {
        try {
          await firstValueFrom(this.brgbService.setNewColor(result));
        } catch (e) {
          console.error("Error setting new color")
        }
      }
    }
}
