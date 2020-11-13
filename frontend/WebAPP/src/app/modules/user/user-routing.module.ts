import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { IndexComponent } from './pages/index/index.component';
import { InterviewDetailComponent } from './pages/interview-detail/interview-detail.component';
import { NotificationsComponent } from './pages/notifications/notifications.component';
import { CurriculumComponent } from './pages/curriculum/curriculum.component';
import { CurriculumViewComponent } from './pages/curriculum-view/curriculum-view.component';

const routes: Routes = [
  { path: '', component: IndexComponent },
  { path: 'entrevistas/:id', component: InterviewDetailComponent },
  { path: 'notificaciones', component: NotificationsComponent },
  { path: 'cv/editar', component: CurriculumComponent },
  { path: 'cv', component: CurriculumViewComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class UserRoutingModule {}
