import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ScrapeService {
  private apiUrl = 'http://127.0.0.1:8000/collaborateurs/scrape/';
  private apiOptionsUrl = 'http://127.0.0.1:8000/collaborateurs/scrapeOptions/';
  private scrape = 'http://127.0.0.1:8000/collaborateurs/actu/';

  constructor(private http: HttpClient) {
  }

  getScrapingData(): Observable<any> {
    return this.http.get(this.apiUrl).pipe(
      map(response => response),
      catchError(this.handleError)
    );
  }

  getSelectOptions(): Observable<any> {
    return this.http.get(this.apiOptionsUrl).pipe(
      map(response => response),
      catchError(this.handleError)
    );
  }

  private handleError(error: any) {
    console.error('An error occurred:', error);
    return throwError(() => new Error('Something bad happened; please try again later.'));
  }

  getActu(): Observable<any> {
    return this.http.get(this.scrape).pipe(
      map(response => response),
      catchError(this.handleError)
    );
  }


}
