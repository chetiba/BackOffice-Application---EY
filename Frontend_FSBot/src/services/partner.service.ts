import { Injectable } from '@angular/core';
import {HttpClient, HttpErrorResponse, HttpHeaders} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class PartnerService {

  private apiUrl = 'http://127.0.0.1:8000/mission';
  private apiUrl1 = 'http://127.0.0.1:8000/collaborateurs';
  private apiUrl2 = 'http://127.0.0.1:8000/client';  // Adjust the base URL as needed

  constructor(private http: HttpClient) {}
getHoursLeft(collabId: number): Observable<any> {
  const url = `${this.apiUrl1}/${collabId}/hours-left/`;
  return this.http.get(url).pipe(catchError(this.handleError));
}

updateMissionMargin(collabMissionId: number, collaboratorId: number, margeMission: number): Observable<any> {
  const url = `${this.apiUrl1}/update-mission-margin/${collabMissionId}/`;
  const headers = new HttpHeaders({
    'Content-Type': 'application/json'
  });

  const body = {
    collaborator_id: collaboratorId,
    marge_mission: margeMission
  };

  return this.http.post(url, body, { headers })
    .pipe(
      catchError(error => {
        console.error('Error during mission margin update:', error);
        return throwError(error);
      })
    );
}

  private handleError1(error: HttpErrorResponse) {
    return throwError(error);
  }


  loadAllCollaborateurs(): Observable<any> {
    const url = `${this.apiUrl1}/load-collaborateurs/`;
    return this.http.get(url)
      .pipe(
        catchError(this.handleError)
      );
  }
getMissionsByCollaborateur(collaborateurId: number): Observable<any> {
  const url = `${this.apiUrl1}/missions-by-collaborator/${collaborateurId}/`;
  return this.http.get(url).pipe(catchError(this.handleError));
}
getMissionsByClient(clientId: number): Observable<any> {
  const url = `${this.apiUrl}/missions-by-client/${clientId}/`;
  return this.http.get(url).pipe(catchError(this.handleError));
}

  loadAllPartners(): Observable<any> {
    const url = `${this.apiUrl1}/load-Partners/`;
    return this.http.get(url)
      .pipe(
        catchError(this.handleError)
      );
  }


  assignMission(managerId: number, missionData: any): Observable<any> {
    const url = `${this.apiUrl}/add-mission/${managerId}/`;
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    return this.http.post(url, JSON.stringify(missionData), { headers })
      .pipe(
        catchError(this.handleError)
      );
  }

  private handleError(error: HttpErrorResponse) {
    return throwError(error);
  }


  aam(clientId: number, managerId: number, missionData: any): Observable<any> {
    const url = `${this.apiUrl}/add-and-assign-mission/client/${clientId}/manager/${managerId}/`;
    return this.http.post(url, missionData).pipe(
      map(response => {
        return response;
      }),
      catchError(error => {
        console.error('Error adding and assigning mission:', error);
        return throwError(error);
      })
    );
  }

  assignMissionToCollaborators(missionId: number, collaboratorIds: number[]): Observable<any> {
    const url = `${this.apiUrl}/assign-mission-to-collaborators/${missionId}/`;
    return this.http.post(url, { collaborator_ids: collaboratorIds }).pipe(
      map(response => {
        return response;
      }),
      catchError(error => {
        console.error('Error assigning mission to collaborators:', error);
        return throwError(error);
      })
    );
  }

  getManagerInfos(): Observable<any> {
    const url = `${this.apiUrl1}/get-id-manager/`;
    return this.http.get(url).pipe(
      map(response => {
        return response;
      }),
      catchError(error => {
        console.error('Error fetching manager IDs:', error);
        return throwError(error);
      })
    );
  }

  getClientIds(): Observable<any> {
    const url = `${this.apiUrl2}/get-client-ids/`; 
    return this.http.get(url).pipe(
      map(response => {
        return response;
      }),
      catchError(error => {
        console.error('Error fetching client IDs:', error);
        return throwError(error);
      })
    );
  }

  getAllMissions(): Observable<any> {
    const url = `${this.apiUrl}/get-all-missions/`;
    return this.http.get(url).pipe(
      map(response => {
        return response;
      }),
      catchError(error => {
        console.error('Error fetching all missions:', error);
        return throwError(error);
      })
    );
  }
}

