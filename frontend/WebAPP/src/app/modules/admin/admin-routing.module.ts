import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ApplicationsIndexComponent } from './applications-index/applications-index.component';
import { IndexComponent } from './index/index.component';
import { UserDetailsComponent } from './user-details/user-details.component';
import { InterviewsIndexComponent } from './interviews-index/interviews-index.component';
import { InterviewsCreateComponent } from './interviews-create/interviews-create.component';
import { InterviewsDetailsComponent } from './interviews-details/interviews-details.component';
import { UserRecommendationsComponent } from './user-recommendations/user-recommendations.component';

const routes: Routes = [
  { 
    path: '',
    component: IndexComponent
  },
  {
    path: 'postulaciones',
    component: ApplicationsIndexComponent
  },
  {
    path: 'usuario/:id',
    component: UserDetailsComponent
  },
  {
    path: 'entrevistas',
    component: InterviewsIndexComponent
  },
  {
    path: 'entrevistas/crear',
    component: InterviewsCreateComponent
  },
  {
    path: 'entrevistas/:id',
    component: InterviewsDetailsComponent
  },
  {
    path: 'buscador',
    component: UserRecommendationsComponent
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class AdminRoutingModule {}
