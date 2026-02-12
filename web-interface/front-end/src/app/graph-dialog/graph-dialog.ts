import { Component } from '@angular/core';
import {LoaderDirective} from '../services/loader/loading-directive';

@Component({
  selector: 'app-graph-dialog',
  imports: [
    LoaderDirective
  ],
  templateUrl: './graph-dialog.html',
  styleUrl: './graph-dialog.scss',
})
export class GraphDialog {

}
