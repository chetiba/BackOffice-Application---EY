import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { ChartsModule } from 'ng2-charts';
import { ChartjsComponent } from './chartjs/chartjs.component';
import { ChartistModule } from 'ng-chartist';
import {FormsModule} from "@angular/forms";
import {HttpClientModule} from "@angular/common/http";

const routes: Routes = [
  { path: 'chartjs', component: ChartjsComponent },
]

@NgModule({
  declarations: [ChartjsComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    ChartsModule,
    ChartistModule,
    FormsModule,
    HttpClientModule

  ]
})
export class ChartsDemoModule { }
