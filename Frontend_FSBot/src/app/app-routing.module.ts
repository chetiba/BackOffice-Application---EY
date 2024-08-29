import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { AdduserComponent } from "./adduser/adduser.component";
import { ChatbotComponent } from "./chatbot/chatbot.component";
import { PositionnementComponent } from "./positionnement/positionnement.component";
import { MissionsComponent } from "./missions/missions.component";
import { ClientComponent } from "./client/client.component";
import { AuthGuard } from '../app/gards/auth.guard';
import {StagiaireComponent} from "./stagiaire/stagiaire.component";
import {EquipeComponent} from "./equipe/equipe.component";

const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard] },
  { path: 'basic-ui', loadChildren: () => import('./basic-ui/basic-ui.module').then(m => m.BasicUiModule), canActivate: [AuthGuard] },
  { path: 'charts', loadChildren: () => import('./charts/charts.module').then(m => m.ChartsDemoModule), canActivate: [AuthGuard] },
  { path: 'forms', loadChildren: () => import('./forms/form.module').then(m => m.FormModule), canActivate: [AuthGuard] },
  { path: 'icons', loadChildren: () => import('./icons/icons.module').then(m => m.IconsModule), canActivate: [AuthGuard] },
  { path: 'apps', loadChildren: () => import('./apps/apps.module').then(m => m.AppsModule), canActivate: [AuthGuard] },
  { path: 'user-pages', loadChildren: () => import('./user-pages/user-pages.module').then(m => m.UserPagesModule) },
  // tslint:disable-next-line:max-line-length
  { path: 'error-pages', loadChildren: () => import('./error-pages/error-pages.module').then(m => m.ErrorPagesModule), canActivate: [AuthGuard] },
  { path: 'adduser', component: AdduserComponent, canActivate: [AuthGuard] },
  { path: 'chatbot', component: ChatbotComponent, canActivate: [AuthGuard] },
  { path: 'positionnement', component: PositionnementComponent, canActivate: [AuthGuard] },
    { path: 'equipe', component: EquipeComponent, canActivate: [AuthGuard] },

  { path: 'missions', component: MissionsComponent, canActivate: [AuthGuard] },
  { path: 'clients', component: ClientComponent, canActivate: [AuthGuard] },
    { path: 'stagiaires', component: StagiaireComponent, canActivate: [AuthGuard] }

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
