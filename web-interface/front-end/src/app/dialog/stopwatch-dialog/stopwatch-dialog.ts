import {Component, Inject, inject} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {MatIconButton} from '@angular/material/button';
import {MatFormField, MatInput, MatLabel} from '@angular/material/input';
import {FormsModule} from '@angular/forms';
import {CappedNumber} from '../../directives/capped-number';

@Component({
  selector: 'app-stopwatch-dialog',
  imports: [
    MatIconButton,
    MatFormField,
    MatLabel,
    FormsModule,
    MatInput,
    CappedNumber
  ],
  templateUrl: './stopwatch-dialog.html',
  styleUrl: './stopwatch-dialog.scss',
})
export class StopwatchDialog {
  dialogRef = inject(MatDialogRef<StopwatchDialog, { startingDuration: number, increaseDuration: number } | null>);
  startingDuration: number = 1;
  increaseDuration: number = 1;

  constructor(@Inject(MAT_DIALOG_DATA) public data: any) { }

  onNoClick(): void {
    this.dialogRef.close(null);
  }

  onYesClick(): void {
    this.dialogRef.close({
      startingDuration: this.startingDuration,
      increaseDuration: this.increaseDuration
    });
  }
}
