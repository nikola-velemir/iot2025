import {Component, Inject, inject, OnInit} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {MatIconButton} from '@angular/material/button';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {DomSanitizer, SafeResourceUrl} from '@angular/platform-browser';

@Component({
  selector: 'app-graph-dialog',
  imports: [
    FormsModule,
    MatIconButton
  ],
  templateUrl: './graph-dialog.html',
  styleUrl: './graph-dialog.scss',
})
export class GraphDialog implements OnInit {
  dialogRef = inject(MatDialogRef<GraphDialog, string | null | undefined>);
  sanitizer = inject(DomSanitizer);
  url = "";
  safeUrl: SafeResourceUrl | undefined;

  constructor(@Inject(MAT_DIALOG_DATA) public data: any) {
    this.url = data.url;
    console.log(this.url);
  }

  ngOnInit() {
    this.safeUrl = this.sanitizer.bypassSecurityTrustResourceUrl(this.url);
  }

  onNoClick(): void {
    this.dialogRef.close(null);
  }
}
