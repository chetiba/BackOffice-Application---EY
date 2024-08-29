import { Component } from '@angular/core';
import { CollabuserService } from '../../../services/collabuser.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  username: string = '';
  password: string = '';

  constructor(private collabuserService: CollabuserService, private router: Router) { }

  login(): void {
    this.collabuserService.login(this.username, this.password).subscribe(
      response => {
        console.log('Login successful:', response);
        // Redirect to dashboard
        this.router.navigate(['/dashboard']);
      },
      error => {
        console.error('Login failed:', error);
        // Handle login error
      }
    );
  }


  logout(): void {
    this.collabuserService.logout();
        this.router.navigate(['/user-pages/login']);
  }
}
