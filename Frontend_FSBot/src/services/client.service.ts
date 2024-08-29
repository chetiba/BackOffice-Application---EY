import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ClientService {
  private apiUrl = 'http://127.0.0.1:8000/client';  // Adjust the base URL as needed

  constructor(private http: HttpClient) { }

  addClient(clientData: any): Observable<any> {
    const url = `${this.apiUrl}/add-client/`; // Ensure it matches the path defined in Django
    return this.http.post(url, clientData);
  }

  getAllClients(): Observable<any> {
    const url = `${this.apiUrl}/get-clients/`; // Ensure it matches the path defined in Django
    return this.http.get(url);
  }
}
