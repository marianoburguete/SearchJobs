import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { IndexComponent } from '../home/pages/index/index.component';
import { DetailComponent } from '../job/pages/detail/detail.component';

const routes: Routes = [{ path: '', component: IndexComponent }, { path: 'detalles/:id', component: DetailComponent}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CompanyRoutingModule { }
