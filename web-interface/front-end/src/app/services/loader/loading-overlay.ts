import {Component} from '@angular/core';
import {MatProgressSpinner} from '@angular/material/progress-spinner';

@Component({
  selector: 'app-loading-overlay',
  standalone: true,
  template: `
    <mat-spinner />
  `,
  imports: [
    MatProgressSpinner
  ],
})
export class LoadingOverlayComponent { }
