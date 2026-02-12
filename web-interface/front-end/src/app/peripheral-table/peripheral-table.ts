import {AfterViewInit, Component, Input, OnInit, ViewChild} from '@angular/core';
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

export interface TableRow {
  name: string;
  type: string;
  peripheralType: PeripheralType;
  col3: string;
  col4: string;
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

  dataSource = new MatTableDataSource();

  ngOnInit() {
    this.dataSource.data = this.dataSourceInput;
  }

  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
  }

  displayedColumns: string[] = ['name', 'type', 'graph', 'actuator-actions'];
}
