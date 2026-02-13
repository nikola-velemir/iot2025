import {Component, inject} from '@angular/core';
import {PeripheralTable, TableRow} from "../../peripheral-table/peripheral-table";
import {MatDialog, MatDialogRef} from '@angular/material/dialog';
import {StopwatchDialog} from '../../dialog/stopwatch-dialog/stopwatch-dialog';
import {firstValueFrom} from 'rxjs';
import {LightColorDialog} from '../../dialog/light-color-dialog/light-color-dialog';
import {BrgbService} from '../../services/brgb-service';

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

    peripherals: TableRow[] = [
      {
        name: 'IR', type: 'Infrared sensor', peripheralType: 'Sensor',
        currentState: "TEST_STATE", grafanaUrl: ""
      },
      {
        name: 'DHT2', type: 'Temperature sensor', peripheralType: 'Sensor',
        currentState: "TEST_STATE", grafanaUrl: ""
      },
      {
        name: 'BGRB', type: 'Colored LED', peripheralType: 'Actuator',
        action: { 'name': "Set light color", callback: () => this.setColorOfBrgb() },
        currentState: "TEST_STATE", grafanaUrl: ""
      },
      {
        name: 'LCD', type: 'LCD display', peripheralType: 'Actuator',
        currentState: "TEST_STATE", grafanaUrl: ""
      },
      {
        name: 'DPIR3', type: 'Motion sensor', peripheralType: 'Sensor',
        currentState: "TEST_STATE", grafanaUrl: ""
      },
      {
        name: 'DHT1', type: 'Temperature sensor', peripheralType: 'Sensor',
        currentState: "TEST_STATE", grafanaUrl: ""
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
