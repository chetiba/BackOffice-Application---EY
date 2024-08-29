import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CollabuserService } from '../../../services/collabuser.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

  addCollaborateurForm: FormGroup;
  isLoading = false; // Variable pour le loader

  constructor(
    private fb: FormBuilder,
    private collabuserService: CollabuserService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.addCollaborateurForm = this.fb.group({
      prenom: ['', Validators.required],
      nom: ['', Validators.required],
      poste: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      departement: ['SSL FS TRANSFORMATION', Validators.required],
      role: ['', Validators.required],
      competences: ['', Validators.required],
      diplome_obtenu: ['', Validators.required],
      institution: ['', Validators.required],
      date: ['', Validators.required],
      image: [null, Validators.required],
      cv: [null, Validators.required]
    });
  }

  onFileSelect(event: any, field: string): void {
    const file = event.target.files[0];
    if (file) {
      this.addCollaborateurForm.get(field).setValue(file);
    }
  }

  onSubmit(): void {
    if (this.addCollaborateurForm.valid) {
      this.isLoading = true; // Affiche le loader
      const formData = new FormData();
      Object.keys(this.addCollaborateurForm.controls).forEach(key => {
        const control = this.addCollaborateurForm.get(key);
        if (control.value instanceof File) {
          formData.append(key, control.value, control.value.name);
        } else {
          formData.append(key, control.value);
        }
      });

      this.collabuserService.addCollaborateur(formData).subscribe({
        next: (response) => {
          alert('Un email vous sera envoyé après validation.');
          this.isLoading = false; // Arrête le loader
          this.router.navigate(['/user-pages/login']);
        },
        error: (error) => {
          console.error('Erreur lors de l\'ajout du collaborateur:', error);
          this.isLoading = false; // Arrête le loader en cas d'erreur
        }
      });
    } else {
      alert('Veuillez remplir tous les champs requis.');
    }
  }
}
