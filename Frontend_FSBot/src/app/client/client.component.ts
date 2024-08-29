import { Component, OnInit } from '@angular/core';
import { ClientService } from '../../services/client.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-client',
  templateUrl: './client.component.html',
  styleUrls: ['./client.component.scss']
})
export class ClientComponent implements OnInit {
  clients: any[] = [];
  filteredClients: any[] = [];
  clientName = '';  // Bound to input in template
  searchTerm: string = ''; // Bound to search input in template
  poste: string = '';

  constructor(
    private clientService: ClientService,
    private toastr: ToastrService
  ) { }

  ngOnInit(): void {
    this.loadAllClients();
    const user = JSON.parse(sessionStorage.getItem('user'));
    if (user) {
      this.poste = user.poste;
    }
  }

  canAccessForms(): boolean {
    return this.poste !== 'Junior Consultant' && this.poste !== 'Senior Consultant';
  }

  loadAllClients(): void {
    this.clientService.getAllClients().subscribe({
      next: (response) => {
        this.clients = response;
        this.filteredClients = response; // Initialize with all clients
      },
      error: (error) => {
        console.error('Failed to retrieve clients', error);
        this.toastr.error('Erreur lors de la récupération des clients.');
      }
    });
  }

  addClient(): void {
    const clientData = { nom: this.clientName.trim() };
    this.clientService.addClient(clientData).subscribe({
      next: (response) => {
        this.toastr.success('Client ajouté avec succès!');
        this.clientName = '';
        this.loadAllClients();  // Recharge la liste après ajout
      },
      error: (error) => {
        console.error('Failed to add client', error);
        this.toastr.error('Échec de l\'ajout du client.', 'Erreur!');
      }
    });
  }

  filterClients(): void {
    this.filteredClients = this.clients.filter(client =>
      client.nom.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }
}
