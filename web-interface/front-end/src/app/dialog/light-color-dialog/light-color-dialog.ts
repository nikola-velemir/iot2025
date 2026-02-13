import {Component, Inject, inject} from '@angular/core';
import {CappedNumber} from "../../directives/capped-number";
import {FormsModule} from "@angular/forms";
import {MatFormField, MatInput, MatLabel} from "@angular/material/input";
import {MatIconButton} from "@angular/material/button";
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';

@Component({
  selector: 'app-light-color-dialog',
    imports: [
        FormsModule,
        MatIconButton
    ],
  templateUrl: './light-color-dialog.html',
  styleUrl: './light-color-dialog.scss',
})
export class LightColorDialog {
  dialogRef = inject(MatDialogRef<LightColorDialog, string | null | undefined>);
  selectedColor: string = '#3f51b5';

  constructor(@Inject(MAT_DIALOG_DATA) public data: any) { }

  onNoClick(): void {
    this.dialogRef.close(null);
  }

  onYesClick(): void {
    this.dialogRef.close(this.selectedColor);
  }
}
