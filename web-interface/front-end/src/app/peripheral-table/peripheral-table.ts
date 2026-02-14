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
import {MatDialog} from '@angular/material/dialog';
import {GraphDialog} from '../dialog/graph-dialog/graph-dialog';
import {PeripheralTabularView} from '../models/PeripheralTabularView';

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
  @Input() dataSourceInput: PeripheralTabularView[] = [];
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
    this.dialog.open(GraphDialog, {
      width: '60vw',
      maxWidth: '60vw',
      height: 'auto',
      data: { url: url }
    });
  }
}
