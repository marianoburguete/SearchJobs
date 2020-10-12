import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CanActivateViaAuthGuard } from './core/guards/can-activate-via-auth.guard';

const routes: Routes = [
  {
    path: '',
    loadChildren: () =>
      import('./modules/home/home.module').then((m) => m.HomeModule),
  },
  {
    path: 'empresa',
    loadChildren: () =>
      import('./modules/company/company.module').then((m) => m.CompanyModule),
  },
  {
    path: 'trabajo',
    loadChildren: () =>
      import('./modules/job/job.module').then((m) => m.JobModule),
  },
  {
    path: 'usuario',
    loadChildren: () =>
      import('./modules/user/user.module').then((m) => m.UserModule),
    canActivate: [CanActivateViaAuthGuard],
  },
  {
    path: 'estadisticas',
    loadChildren: () =>
      import('./modules/stats/stats.module').then((m) => m.StatsModule),
  },
  {
    path: 'admin',
    loadChildren: () =>
      import('./modules/admin/admin.module').then((m) => m.AdminModule),
    canActivate: [CanActivateViaAuthGuard],
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
