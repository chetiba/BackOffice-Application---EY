import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CollabuserService } from '../../../services/collabuser.service';

@Component({
  selector: 'app-change-password',
  templateUrl: './change-password.component.html',
  styleUrls: ['./change-password.component.scss']
})
export class ChangePasswordComponent {
  newPassword: string = '';
  uidb64: string = '';
  token: string = '';

  constructor(private router: Router, private collabuserService: CollabuserService) { }

  changePassword(): void {
    this.collabuserService.confirmResetPassword(this.uidb64, this.token, this.newPassword).subscribe({
      next: response => {
        console.log('Mot de passe changé avec succès:', response);
        this.router.navigate(['/user-pages/login']);
      },
      error: error => {
        console.error('Échec de la réinitialisation du mot de passe:', error);
      }
    });
  }
}
