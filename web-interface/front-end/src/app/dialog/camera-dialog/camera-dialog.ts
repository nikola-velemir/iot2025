import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-camera-dialog',
  imports: [],
  templateUrl: './camera-dialog.html',
  styleUrl: './camera-dialog.scss',
})
export class CameraDialog {
  cameraIp = "http://192.168.0.7:9000/?action=stream"
}
