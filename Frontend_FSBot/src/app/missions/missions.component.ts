import { Component, OnInit } from '@angular/core';
import { PartnerService } from '../../services/partner.service';
import { NgForm } from '@angular/forms';
import { ToastrService } from 'ngx-toastr';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-missions',
  templateUrl: './missions.component.html',
  styleUrls: ['./missions.component.scss']
})
export class MissionsComponent implements OnInit {
  clients: any[] = [];
  managers: any[] = [];
  partners: any[] = [];
  collaborateurs: any[] = [];
  missions: any[] = [];
  selectedClientId: number;
  selectedManagerId: number;
  selectedPartnerId: number;
  deliveryTeamIds: number[] = [];
  marges: { [key: number]: number } = {};
  margeMissionManager = 1;
  selectedCollaborateurId: number;
  isPlaceholderHidden = false;
  missionsByCollaborateur: any[] = [];
  missionsByClient: any[] = [];
  selectedCollaborateur: any = null;
  selectedClient: any = null;
  poste = '';
  managerName = '';
  managerId = 0;

  constructor(private partnerService: PartnerService, private toastr: ToastrService) {
  }

  ngOnInit(): void {
    this.loadClients();
    this.loadManagers();
    this.loadPartners();
    this.loadMissions();
    this.loadCollaborateurs();
    const user = JSON.parse(sessionStorage.getItem('user'));
    if (user) {
      this.poste = user.poste;
    }
    this.loadInitialData();
    this.loadManagerDetails();
    this.loadManagerId();

  }

  loadManagerDetails() {
    const userDataString = sessionStorage.getItem('user');
    if (userDataString) {
      const userData = JSON.parse(userDataString);
      const prenom = userData.prenom;
      const nom = userData.nom;
      if (prenom && nom) {
        this.managerName = `${prenom} ${nom}`;
      } else {
        this.managerName = 'Manager name not found';
      }
    } else {
      this.managerName = 'Manager details not found in session';
    }
  }

  onDeliveryTeamSelect(selectedId: any): void {
    const id = +selectedId;
    if (!this.deliveryTeamIds.includes(id)) {
      this.deliveryTeamIds.push(id);
      this.marges[id] = 0;
    }
    this.isPlaceholderHidden = true;
  }

  canAccessForms(): boolean {
    return this.poste !== 'Junior Consultant' && this.poste !== 'Senior Consultant';
  }

  adjustMargeValue() {
    if (this.margeMissionManager > 40) {
      this.margeMissionManager = 40;
    } else if (this.margeMissionManager < 1) {
      this.margeMissionManager = 1;
    }
  }

  adjustMemberMarge(memberId: number) {
    if (this.marges[memberId] > 40) {
      this.marges[memberId] = 40;
    } else if (this.marges[memberId] < 1) {
      this.marges[memberId] = 1;
    }
  }

  loadInitialData() {
    const managerInfo = sessionStorage.getItem('user');
    if (managerInfo) {
      const userData = JSON.parse(managerInfo);
      this.selectedManagerId = userData.id;
      this.managerName = `${userData.prenom} ${userData.nom}`;
    }
  }

  removeDeliveryTeamMember(selectedId: number): void {
    const index = this.deliveryTeamIds.indexOf(selectedId);
    if (index !== -1) {
      this.deliveryTeamIds.splice(index, 1);
      delete this.marges[selectedId];
    }
  }

  loadClients(): void {
    this.partnerService.getClientIds().subscribe(
      data => {
        this.clients = data;
      },
      error => {
        console.error('Erreur lors de la récupération des clients:', error);
      }
    );
  }

  loadManagers(): void {
    this.partnerService.getManagerInfos().subscribe(
      data => {
        this.managers = data;
      },
      error => {
        console.error('Erreur lors de la récupération des managers:', error);
      }
    );
  }

  loadPartners(): void {
    this.partnerService.loadAllPartners().subscribe(
      data => {
        this.partners = data;
      },
      error => {
        console.error('Erreur lors de la récupération des partenaires:', error);
      }
    );
  }

  loadMissions(): void {
    this.partnerService.getAllMissions().subscribe({
      next: (data) => {
        console.log('Missions loaded:', data);
        this.missions = data;
      },
      error: (error) => {
        console.error('Failed to load missions:', error);
        this.toastr.error('Failed to load missions.', 'Error');
      }
    });
  }


  onCollaborateurSelect(event: any): void {
    const collaborateurId = event.target.value;
    this.selectedCollaborateur = this.collaborateurs.find(c => c.id === +collaborateurId);
    this.partnerService.getMissionsByCollaborateur(collaborateurId).subscribe(
      data => {
        console.log('Missions by Collaborateur:', data);
        this.missionsByCollaborateur = data;
      },
      error => {
        console.error('Erreur lors de la récupération des missions:', error);
        this.toastr.error('Erreur lors de la récupération des missions.', 'Erreur');
      }
    );
  }

  onClientSelect(event: any): void {
    const clientId = event.target.value;
    this.selectedClient = this.clients.find(c => c.id === +clientId);
    this.partnerService.getMissionsByClient(clientId).subscribe(
      data => {
        console.log('Missions by Client:', data);
        this.missionsByClient = data;
      },
      error => {
        console.error('Erreur lors de la récupération des missions:', error);
        this.toastr.error('Erreur lors de la récupération des missions.', 'Erreur');
      }
    );
  }

  loadCollaborateurs(): void {
    this.partnerService.loadAllCollaborateurs().subscribe({
      next: (collaborateurs) => {
        this.collaborateurs = collaborateurs;
        this.collaborateurs.forEach(collab => {
          this.partnerService.getHoursLeft(collab.id).subscribe({
            next: (data) => {
              collab.hoursLeft = `${data.hours_left} h/sem`;
            },
            error: (error) => {
              console.error('Erreur lors de la récupération des heures restantes pour', collab.prenom, collab.nom, ':', error);
              this.toastr.error('Erreur lors de la récupération des heures restantes.');
            }
          });
        });
      },
      error: (error) => {
        console.error('Erreur lors de la récupération des collaborateurs:', error);
        this.toastr.error('Erreur lors de la récupération des collaborateurs');
      }
    });
  }

  onSubmit(form: NgForm): void {
    if (form.valid) {
      const managerId = this.managerId
      const missionData = {
        client_id: this.selectedClientId,
        nom_projet: form.value.nom_projet,
        date_debut: new Date(form.value.date_debut).toISOString().split('T')[0],
        date_fin: new Date(form.value.date_fin).toISOString().split('T')[0],
        partner_id: this.selectedPartnerId,
        delivery_team_ids: this.deliveryTeamIds,
        marges: this.marges,
        marge_mission_manager: this.margeMissionManager
      };

      if (managerId > 0) {
        this.partnerService.assignMission(managerId, missionData).subscribe(
          response => {
            if (response.message) {
              this.toastr.success(response.message, 'Succès');
            }
            form.reset();
            this.deliveryTeamIds = [];
            this.marges = {};
            this.margeMissionManager = 1;
            this.loadMissions();
          },
          (error: HttpErrorResponse) => {
            if (error.status === 400 && error.error) {
              const backendError = error.error;
              this.toastr.error(backendError.erreur, 'Erreur');
              if (backendError.détails && Array.isArray(backendError.détails)) {
                backendError.détails.forEach((detail: string) => {
                  this.toastr.error(detail, 'Erreur');
                });
              }
            } else {
              this.toastr.error('Une erreur inattendue est survenue.', 'Erreur');
            }
          }
        );
      } else {
        this.toastr.error('Session information is missing. Please log in again.', 'Error');
      }
    } else {
      this.toastr.error('Veuillez remplir correctement tous les champs obligatoires.', 'Formulaire invalide');
    }
  }

  loadManagerId() {
    const userString = sessionStorage.getItem('user');
    if (userString) {
      const user = JSON.parse(userString);
      this.managerId = user.id;
    }
  }

  getCollaborateurName(id: number): string {
    const collaborateur = this.collaborateurs.find(c => c.id === id);
    return collaborateur ? `${collaborateur.prenom} ${collaborateur.nom}` : 'Inconnu';
  }

  updateMargin(memberId: number, value: number): void {
    this.marges[memberId] = Math.max(1, Math.min(40, value));
  }

updateMissionMargin(mission: any, form: NgForm): void {
  const collabMissionId = mission.collabmission_id;
  const collaboratorId = mission.collaborateur.id;
  const newMargeMission = mission.marge_mission;

  if (!collabMissionId) {
    this.toastr.error('ID de la mission non défini.', 'Erreur');
    return;
  }

  if (newMargeMission >= 1 && newMargeMission <= 40) {
    this.partnerService.updateMissionMargin(collabMissionId, collaboratorId, newMargeMission).subscribe({
      next: (response) => {
        this.toastr.success('Marge mission mise à jour avec succès.', 'Succès');
        form.reset();
        this.resetTeamMembers();
      },
      error: (error: HttpErrorResponse) => {
        this.toastr.error('Erreur lors de la mise à jour de la marge de mission.', 'Erreur');
      }
    });
  } else {
    this.toastr.error('La marge doit être entre 1 et 40.', 'Valeur invalide');
  }
}
resetTeamMembers(): void {
  this.deliveryTeamIds = [];
  this.marges = {};
}

}
