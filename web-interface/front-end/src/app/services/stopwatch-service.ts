import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class StopwatchService {
    http = inject(HttpClient);

    initializeStopwatch(totalMinutes: number, rampUpSeconds: number): Observable<void> {
        return this.http.post<void>("http://localhost:8080/api/stopwatch/initialize",
          {
            "totalMinutes": totalMinutes,
            "rampUpSeconds": rampUpSeconds
          }
        )
    }
}
