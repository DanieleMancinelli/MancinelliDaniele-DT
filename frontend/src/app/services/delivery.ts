import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DeliveryService {
  // Sostituisci con l'URL della tua porta 5000
  private apiUrl = 'https://animated-space-doodle-g4xv64xp5jqwhv64v-5000.app.github.dev/deliveries';

  constructor(private http: HttpClient) { }

  getDeliveries(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

  addDelivery(delivery: any): Observable<any> {
    return this.http.post(this.apiUrl, delivery);
  }

  updateStatus(id: number, status: string): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}/status`, { status: status });
  }
}