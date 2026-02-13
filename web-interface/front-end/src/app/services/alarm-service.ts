import {inject, Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class AlarmService {
    http = inject(HttpClient);

    turnOffAlarm(): Observable<void> {
        return this.http.post<void>("http://localhost:8080/api/alarm/off", {})
    }
}
