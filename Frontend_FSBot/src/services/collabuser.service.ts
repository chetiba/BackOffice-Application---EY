import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

// Remove Content-Type header when dealing with FormData
const httpOptions = {
  // No headers needed for 'Content-Type'
};

@Injectable({
  providedIn: 'root'
})
export class CollabuserService {

  private apiUrl = 'http://127.0.0.1:8000/collaborateurs';

  constructor(private http: HttpClient) { }

  login(username: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/login/`, { username, password }, httpOptions)
      .pipe(
        map((response: any) => {
          sessionStorage.setItem('user', JSON.stringify(response.user));
          return response.user;
        }),
        catchError(this.handleError)
      );
  }


  logout(): Observable<any> {
    const username = this.getUsername();
    return this.http.post(`${this.apiUrl}/logout/`, { username }, httpOptions)
      .pipe(
        map(response => {
          sessionStorage.removeItem('user');
          return response;
        }),
        catchError(this.handleError)
      );
  }

  private handleError(error: any): Observable<never> {
    console.error('An error occurred:', error);
    return throwError('Something bad happened; please try again later.');
  }
 getUserData(): any {
    const userData = sessionStorage.getItem('user');
    return userData ? JSON.parse(userData) : null;
  }
getUsername(): string {
  const user = this.getUserData();
  return user ? user.username : '';
}

  getPrenom(): string {
    const user = this.getUserData();
    return user ? user.prenom : '';
  }

  getId(): number {
    const user = this.getUserData();
    return user ? user.id : null;
  }
  getFullName(): string {
    const user = this.getUserData();
    if (!user) return '';
    const prenom = user.prenom ? this.capitalizeFirstLetter(user.prenom) : '';
    const nom = user.nom ? this.capitalizeFirstLetter(user.nom) : '';
    return `${prenom} ${nom}`.trim();
  }

  private capitalizeFirstLetter(inputstring: string) {
    return inputstring.charAt(0).toUpperCase() + inputstring.slice(1).toLowerCase();
  }

  getNom(): string {
    const user = this.getUserData();
    return user ? user.nom : '';
  }

  getPoste(): string {
    const user = this.getUserData();
    return user ? user.poste : '';
  }

  getDepartement(): string {
    const user = this.getUserData();
    return user ? user.departement : '';
  }

  getEmail(): string {
    const user = this.getUserData();
    return user ? user.email : '';
  }

  getAccessToken(): string {
    const user = this.getUserData();
    return user ? user.access_token : '';
  }

  getRefreshToken(): string {
    const user = this.getUserData();
    return user ? user.refresh_token : '';
  }

  addCollaborateur(collaborateurData: FormData): Observable<any> {
    return this.http.post(`${this.apiUrl}/add/`, collaborateurData)
      .pipe(
        catchError(this.handleError)
      );
  }
resetPassword(email: string): Observable<any> {
  return this.http.post(`${this.apiUrl}/reset-password/`, { email }, httpOptions)
    .pipe(
      map(response => response),
      catchError(this.handleError)
    );
}
confirmResetPassword(uidb64: string, token: string, password: string): Observable<any> {
  const url = `${this.apiUrl}/reset-confirm/${uidb64}/${token}/`;
  return this.http.post(url, { password }, httpOptions)
    .pipe(
      map(response => response),
      catchError(this.handleError)
    );
}
  getAllUsers(): Observable<any> {
    return this.http.get(`${this.apiUrl}/getusers/`)
      .pipe(
        map(response => {
          return response;
        }),
        catchError(this.handleError)
      );
  }

  editUser(userId: number, userData: any): Observable<any> {
    const url = `${this.apiUrl}/edit-user/${userId}/`;
    return this.http.put(url, userData, httpOptions)
      .pipe(
        map(response => response),
        catchError(this.handleError)
      );
  }
  deleteUser(userId: number): Observable<any> {
    const url = `${this.apiUrl}/delete-user/${userId}/`;
    return this.http.delete(url, httpOptions)
      .pipe(
        map(response => response),
        catchError(this.handleError)
      );
  }
  validerInscription(collabId: number): Observable<any> {
    const url = `${this.apiUrl}/valider-inscription/${collabId}/`;
    return this.http.post(url, {}).pipe(
      map(response => response),
      catchError(this.handleError)
    );
  }
  getCollaborateurs(): Observable<any> {
    return this.http.get(`${this.apiUrl}/getCollaborateurs/`, httpOptions).pipe(
      map(response => {
        return response;
      }),
      catchError(error => {
        console.error('Error fetching collaborateurs:', error);
        return throwError(error);
      })
    );
  }


}

