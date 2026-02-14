import {Injectable, signal} from '@angular/core';
import {EMPTY_REAL_TIME_DATA, RealTimeData} from '../models/GlobalState';

@Injectable({
  providedIn: 'root',
})
export class GlobalStateService {
  private state = signal<RealTimeData>(EMPTY_REAL_TIME_DATA);

  public readonly data = this.state.asReadonly();

  setGlobalState(newState: RealTimeData) {
    this.state.set(newState);
  }
}
