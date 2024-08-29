import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { Routes, RouterModule } from '@angular/router';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import { ForgetPassComponent } from './forget-pass/forget-pass.component';
import { ChangePasswordComponent } from "./change-password/change-password.component";  // Assurez-vous que le chemin est correct

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'reset', component: ForgetPassComponent },
  { path: 'change-password', component: ChangePasswordComponent }  // Assurez-vous que cette route est correcte
];

@NgModule({
  declarations: [
    LoginComponent,
    RegisterComponent,
    ForgetPassComponent,
    ChangePasswordComponent  // Ajoutez-le ici
  ],
    imports: [
        CommonModule,
        RouterModule.forChild(routes),
        FormsModule,
        ReactiveFormsModule
    ]
})
export class UserPagesModule { }
