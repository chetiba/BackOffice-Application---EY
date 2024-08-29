import { Component, OnInit } from '@angular/core';
import { CollabuserService } from '../../services/collabuser.service';

@Component({
  selector: 'app-adduser',
  templateUrl: './adduser.component.html',
  styleUrls: ['./adduser.component.scss']
})
export class AdduserComponent implements OnInit {
  collaborateurs: any[] = [];  // Variable pour stocker la liste des collaborateurs
  isLoading = false; // Loader pour la validation

  constructor(private collabuserService: CollabuserService) { }

  ngOnInit(): void {
    this.fetchCollaborateurs();  // Récupérer les collaborateurs au chargement
  }

  // Méthode pour récupérer la liste des collaborateurs
  fetchCollaborateurs(): void {
    this.collabuserService.getCollaborateurs().subscribe({
      next: (response) => {
        this.collaborateurs = response;
      },
      error: (error) => {
        console.error('Erreur lors de la récupération des collaborateurs:', error);
      }
    });
  }

  // Méthode pour valider l'inscription d'un collaborateur
  validerInscription(collabId: number): void {
    this.isLoading = true;
    this.collabuserService.validerInscription(collabId).subscribe({
      next: () => {
        alert('Collaborateur validé avec succès.');
        this.isLoading = false;
        this.fetchCollaborateurs();  // Rafraîchir la liste après validation
      },
      error: (error) => {
        console.error('Erreur lors de la validation du collaborateur:', error);
        this.isLoading = false;
      }
    });
  }
}
