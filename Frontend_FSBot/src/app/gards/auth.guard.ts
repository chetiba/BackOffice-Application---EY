import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { CollabuserService } from '../../services/collabuser.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(private collabUserService: CollabuserService, private router: Router) {}

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {

    const token = this.collabUserService.getAccessToken();

    if (!token) {
      // Redirect to the login page if the user is not authenticated
      this.router.navigate(['user-pages/login']);
      return false;
    }

    return true; // Allow access if the user is authenticated
  }
}
