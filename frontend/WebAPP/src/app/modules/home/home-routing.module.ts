import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { IndexComponent } from './pages/index/index.component';
import { AboutComponent } from './pages/about/about.component';
import { LoginComponent } from './pages/login/login.component';
import { RegisterComponent } from './pages/register/register.component';
import { CanActivateViaAuthGuard } from '../../core/guards/can-activate-via-auth.guard';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  {
    path: 'home',
    component: IndexComponent
  },
  {
    path: 'login',
    component: LoginComponent,
    canActivate: [CanActivateViaAuthGuard]
  },
  {
    path: 'registro',
    component: RegisterComponent,
    canActivate: [CanActivateViaAuthGuard]
  },
  {
    path: 'acerca',
    component: AboutComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class HomeRoutingModule {}
