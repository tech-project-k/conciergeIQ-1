import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { HomeComponent } from './pages/home/home.component';
import { LoginComponent } from './components/login/login.component';
import { MapPageComponent } from './pages/map-page/map-page.component';
import { AiChatComponent } from './components/ai-chat/ai-chat.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';

const routes: Routes = [

  {
    path: '',
    component: HomeComponent
  },

  {
    path: 'login',
    component: LoginComponent
  },

  {
    path: 'map',
    component: MapPageComponent
  },
  {
    path: 'ai-chat',
    component: AiChatComponent
  },
  {
    path: 'dashboard',
    component: DashboardComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }