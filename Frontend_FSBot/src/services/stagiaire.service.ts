import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StagiaireService {
  private apiUrl = 'http://localhost:8000/stagiaire';  // Change this URL based on your actual server URL

  constructor(private http: HttpClient) { }

createStagiaire(stagiaire: any): Observable<any> {
  return this.http.post(`${this.apiUrl}/create/`, stagiaire, {
    headers: { 'Content-Type': 'application/json' }
  });
}

  listStagiaires(): Observable<any> {
    return this.http.get(`${this.apiUrl}/list/`);
  }

  getStagiairesByCollaborateur(collaborateurId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/retrieve-by-collaborateur/${collaborateurId}/`);
  }

// Angular service
updateStagiaire(id: number, stagiaire: any): Observable<any> {
  return this.http.post(`${this.apiUrl}/update/${id}/`, stagiaire, {
    headers: { 'Content-Type': 'application/json' }
  });
}

  deleteStagiaire(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/delete/${id}/`);
  }
}
