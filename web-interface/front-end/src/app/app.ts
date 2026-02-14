import {ChangeDetectorRef, Component, inject, NgZone, OnDestroy, OnInit} from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {Navbar} from './navbar/navbar';
import {LoaderDirective} from './services/loader/loading-directive';
import {WebSocketService} from './services/web-socket-service';
import {RealTimeData} from './models/GlobalState';
import {GlobalStateService} from './services/global-state-service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Navbar, LoaderDirective],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App implements OnDestroy, OnInit {
  private realTimeSubscription: any;
  private isWsConnecting = false;
  private wsService = inject(WebSocketService);
  private globalState = inject(GlobalStateService);
  private cdr = inject(ChangeDetectorRef);
  private zone = inject(NgZone);

  ngOnInit() {
    this.startRealTimeUpdates();
  }

  ngOnDestroy() {
    if (this.realTimeSubscription) {
      this.stopRealTimeUpdates();
      this.wsService.disconnect();
    }
  }

  private startRealTimeUpdates() {
    const performSubscription = () => {
      this.realTimeSubscription = this.wsService.subscribe('/data/user', (payload) =>
        this.handleWsUpdate(payload)
      );
    };

    if (this.wsService.isConnected()) {
      performSubscription();
      return;
    }

    if (this.isWsConnecting) return;
    this.isWsConnecting = true;

    this.wsService.connect(() => {
      this.isWsConnecting = false;
      performSubscription();
    });
  }

  private stopRealTimeUpdates() {
    if (this.realTimeSubscription) {
      this.realTimeSubscription.unsubscribe();
      this.realTimeSubscription = null;
    }
  }

  private handleWsUpdate(payload: RealTimeData) {
    console.log(payload);
    this.zone.run(() => {
      this.globalState.setGlobalState(payload);
      this.cdr.detectChanges();
    })
  }
}
