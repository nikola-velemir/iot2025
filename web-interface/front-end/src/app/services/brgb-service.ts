import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class BrgbService {
    http = inject(HttpClient);

    setNewColor(color: string): Observable<void> {
        return this.http.post<void>("http://localhost:8080/api/brgb/set", {"color": color})
    }
}
