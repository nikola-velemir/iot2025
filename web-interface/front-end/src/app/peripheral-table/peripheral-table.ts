import {AfterViewInit, Component, inject, Input, OnInit, ViewChild} from '@angular/core';
import {
  MatCell, MatCellDef,
  MatColumnDef,
  MatHeaderCell, MatHeaderCellDef,
  MatHeaderRow,
  MatHeaderRowDef,
  MatRow,
  MatRowDef, MatTable, MatTableDataSource
} from '@angular/material/table';
import {MatSort, MatSortModule} from '@angular/material/sort';
import {MatDialog, MatDialogRef} from '@angular/material/dialog';
import {StopwatchDialog} from '../dialog/stopwatch-dialog/stopwatch-dialog';
import {firstValueFrom} from 'rxjs';
import {GraphDialog} from '../dialog/graph-dialog/graph-dialog';

export interface TableRow {
  name: string;
  type: string;
  peripheralType: PeripheralType;
  action?: {
    name: string,
    callback: () => void;
  };
  currentState: string;
  grafanaUrl: string;
}

export type PeripheralType = "Sensor" | "Actuator";

@Component({
  selector: 'app-peripheral-table',
  imports: [
    MatRow,
    MatHeaderRow,
    MatHeaderRowDef,
    MatRowDef,
    MatHeaderCell,
    MatColumnDef,
    MatCell,
    MatHeaderCellDef,
    MatCellDef,
    MatTable,
    MatSortModule
  ],
  templateUrl: './peripheral-table.html',
  styleUrl: './peripheral-table.scss',
})
export class PeripheralTable implements AfterViewInit, OnInit {
  @Input() dataSourceInput: TableRow[] = [];
  @ViewChild(MatSort) sort!: MatSort;

  dialog = inject(MatDialog);
  dataSource = new MatTableDataSource();
  anyAction: boolean = false;
  displayedColumns: string[] = [];

  ngOnInit() {
    this.dataSource.data = this.dataSourceInput;
    this.anyAction = this.dataSourceInput.some(t => t.action !== undefined);

    if (this.anyAction) {
      this.displayedColumns = ['name', 'type', 'graph', 'actuator-actions', 'current-state'];
    } else {
      this.displayedColumns = ['name', 'type', 'graph', 'current-state'];
    }
  }

  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
  }

  async openGrafanaGraph(url: string) {
    const dialogRef: MatDialogRef<GraphDialog, null | undefined> = this.dialog.open(GraphDialog, {
      height: '600px',
    });
  }
}
