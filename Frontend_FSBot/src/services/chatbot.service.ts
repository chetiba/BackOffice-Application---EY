import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {
  private apiUrl = 'http://127.0.0.1:8000/collaborateurs/chat_with_rasa/';

  constructor(private http: HttpClient) {}

  sendMessage(message: string, sender: string = 'default_user'): Observable<any> {
    const body = JSON.stringify({ message, sender });
    return this.http.post(this.apiUrl, body, { headers: new HttpHeaders({ 'Content-Type': 'application/json' }) })
      .pipe(
        map(response => {
          console.log('Response from API:', response);  // Log the raw response from the API
          return response;
        }),
        catchError(error => {
          console.error('API Error:', error);  // Log detailed error
          return throwError(() => new Error('Communication error with the chatbot API: ' + error.message));
        })
      );
  }
}
