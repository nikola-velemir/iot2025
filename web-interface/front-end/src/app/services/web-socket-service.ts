import { Injectable } from '@angular/core';
import * as StompJs from '@stomp/stompjs';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  private stompClient: StompJs.Client | null = null;
  private state: BehaviorSubject<any> = new BehaviorSubject<any>(null);
  private readonly BASE_URL = 'ws://localhost:8080/api/socket';

  constructor() { }

  connect(onConnectCallback: () => void): void {
    this.stompClient = new StompJs.Client({
      brokerURL: this.BASE_URL,
      reconnectDelay: 5000,
      heartbeatIncoming: 4000,
      heartbeatOutgoing: 4000,
    });

    this.stompClient.onConnect = (frame:any) => {
      this.state.next(true);
      onConnectCallback();
    };

    this.stompClient.onStompError = (frame:any) => {
      console.error('Broker reported error: ' + frame.headers['message']);
      console.error('Additional details: ' + frame.body);
    };

    this.stompClient.activate();
  }

  public isConnected(): boolean {
    return this.stompClient !== null && this.stompClient.connected;
  }

  subscribe(topic: string, callback: (payload: any) => void): any {
    if (this.isConnected()) {
      return this.stompClient!.subscribe(topic, (message:any) => callback(JSON.parse(message.body)));
    } else {
      console.error("STOMP client not connected yet.");
    }
  }

  disconnect(): void {
    if (this.stompClient === null) {
      console.error("Cannot disconnect to empty stomp client");
    }

    if (this.stompClient) {
      this.stompClient.deactivate();
    }
  }
}
