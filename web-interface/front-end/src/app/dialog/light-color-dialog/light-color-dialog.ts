import {Component, Inject, inject} from '@angular/core';
import {FormsModule} from "@angular/forms";
import {MatFormField} from "@angular/material/input";
import {MatIconButton} from "@angular/material/button";
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {MatOption, MatSelect, MatSelectTrigger} from '@angular/material/select';

interface PresetColor {
  name: string;
  hex: string;
}

@Component({
  selector: 'app-light-color-dialog',
  imports: [
    FormsModule,
    MatIconButton,
    MatFormField,
    MatSelect,
    MatOption,
    MatSelectTrigger,
  ],
  templateUrl: './light-color-dialog.html',
  styleUrl: './light-color-dialog.scss',
})
export class LightColorDialog {
  dialogRef = inject(MatDialogRef<LightColorDialog, string | null | undefined>);
  public readonly COLORS: PresetColor[] = [
    { name: 'WHITE',  hex: '#FFFFFF' },
    { name: 'RED',    hex: '#FF0000' },
    { name: 'GREEN',  hex: '#008000' },
    { name: 'BLUE',   hex: '#0000FF' },
    { name: 'YELLOW', hex: '#FFFF00' },
    { name: 'PURPLE', hex: '#800080' },
    { name: 'CYAN',   hex: '#00FFFF' }
  ];

  selectedColor: string = this.COLORS[0].name;

  getSelectedColorColor(): string {
    const color = this.COLORS.find(c => c.name === this.selectedColor);
    return color ? color.hex : '';
  }

  constructor(@Inject(MAT_DIALOG_DATA) public data: any) { }

  onNoClick(): void {
    this.dialogRef.close(null);
  }

  onYesClick(): void {
    this.dialogRef.close(this.selectedColor);
  }
}
