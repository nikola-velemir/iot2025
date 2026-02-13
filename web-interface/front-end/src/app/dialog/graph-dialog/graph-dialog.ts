import {Component, Inject, inject} from '@angular/core';
import {LoaderDirective} from '../../services/loader/loading-directive';
import {FormsModule} from '@angular/forms';
import {MatIconButton} from '@angular/material/button';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';

@Component({
  selector: 'app-graph-dialog',
  imports: [
    FormsModule,
    MatIconButton
  ],
  templateUrl: './graph-dialog.html',
  styleUrl: './graph-dialog.scss',
})
export class GraphDialog {
  dialogRef = inject(MatDialogRef<GraphDialog, string | null | undefined>);
  url = "";

  onNoClick(): void {
    this.dialogRef.close(null);
  }
}
