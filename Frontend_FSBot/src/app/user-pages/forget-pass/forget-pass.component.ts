import { Component, OnInit } from '@angular/core';
import { CollabuserService } from '../../../services/collabuser.service'; // Assurez-vous que le chemin est correct

@Component({
  selector: 'app-forget-pass',
  templateUrl: './forget-pass.component.html',
  styleUrls: ['./forget-pass.component.scss']
})
export class ForgetPassComponent  {
  email: string;

  constructor(private userService: CollabuserService) {}

  resetPassword() {
    this.userService.resetPassword(this.email).subscribe({
      next: response => {
        console.log('Instructions sent to email:', response);
        // Vous pouvez ajouter une notification à l'utilisateur ici
      },
      error: error => {
        console.error('Failed to send email:', error);
        // Gérer les erreurs ici
      }
    });
  }
}
