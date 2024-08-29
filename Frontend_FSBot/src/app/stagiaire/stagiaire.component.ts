import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { StagiaireService } from '../../services/stagiaire.service';

@Component({
  selector: 'app-stagiaire',
  templateUrl: './stagiaire.component.html',
  styleUrls: ['./stagiaire.component.scss']
})
export class StagiaireComponent implements OnInit {
  stagiaires = [];
  newStagiaire = { prenom: '', nom: '', email: '', sujet_pfe: '', etat_avancement: 0, collaborateur_id: this.getId() };
  updateStagiaire: any;

  constructor(private stagiaireService: StagiaireService, private toastr: ToastrService) { }

  ngOnInit(): void {
    this.loadStagiaires();
  }

  getId(): number {
    const user = this.getUserData();
    return user ? user.id : null;
  }

  getUserData(): any {
    const userData = sessionStorage.getItem('user');
    return userData ? JSON.parse(userData) : null;
  }

  addStagiaire(): void {
    this.newStagiaire.collaborateur_id = this.getId();
    if (this.validateStagiaire(this.newStagiaire)) {
      this.stagiaireService.createStagiaire(this.newStagiaire).subscribe(
        response => {
          this.loadStagiaires();
          this.toastr.success('Stagiaire ajouté avec succès.');
          this.resetNewStagiaire();
        },
        error => {
          this.toastr.error('Erreur lors de l\'ajout du stagiaire');
          console.error('Erreur lors de l\'ajout du stagiaire', error);
        }
      );
    } else {
      this.toastr.error('Tous les champs sont requis, y compris l\'identifiant du collaborateur.');
    }
  }

  validateStagiaire(stagiaire: any): boolean {
    return stagiaire.prenom && stagiaire.nom && stagiaire.email && stagiaire.sujet_pfe && stagiaire.collaborateur_id;
  }

  loadStagiaires(): void {
    this.stagiaireService.getStagiairesByCollaborateur(this.getId()).subscribe(
      data => {
        this.stagiaires = data.map(stagiaire => ({
          ...stagiaire,
          etat_avancement: stagiaire.etat_avancement
        }));
      },
      error => {
        this.toastr.error('Erreur lors de la récupération des stagiaires.');
        console.error('Error while fetching stagiaires:', error);
      }
    );
  }

  deleteStagiaire(id: number): void {
    this.stagiaireService.deleteStagiaire(id).subscribe(
      response => {
        this.loadStagiaires();  // Refresh the list after deletion
        this.toastr.success('Stagiaire supprimé avec succès.');
      },
      error => {
        this.toastr.error('Erreur lors de la suppression du stagiaire.');
        console.error('Erreur lors de la suppression du stagiaire', error);
      }
    );
  }

  prepareUpdate(stagiaire: any): void {
    this.updateStagiaire = { ...stagiaire };
    console.log('Preparing update for:', this.updateStagiaire);
  }

  updateEtatAvancement(stagiaire: any): void {
    if (stagiaire.collaborateur_id) {
      this.stagiaireService.updateStagiaire(stagiaire.id, stagiaire).subscribe(
        response => {
          this.loadStagiaires(); // Refresh the list to see changes
          this.toastr.success('Mise à jour réussie.');
        },
        error => {
          this.toastr.error('Erreur lors de la mise à jour.');
          console.error('Erreur lors de la mise à jour', error);
        }
      );
    } else {
      this.toastr.error('L\'identifiant du collaborateur est manquant dans les données de mise à jour.');
    }
  }

  resetNewStagiaire(): void {
    this.newStagiaire = { prenom: '', nom: '', email: '', sujet_pfe: '', etat_avancement: 0, collaborateur_id: this.getId() };
  }

  trackByStagiaireId(index: number, stagiaire: any): number {
    return stagiaire.id;
  }
}
