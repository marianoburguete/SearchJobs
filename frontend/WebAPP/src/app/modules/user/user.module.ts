import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { UserRoutingModule } from './user-routing.module';
import { IndexComponent } from './pages/index/index.component';
import { InterviewDetailComponent } from './pages/interview-detail/interview-detail.component';
import { CurriculumComponent } from './pages/curriculum/curriculum.component';
import { NotificationsComponent } from './pages/notifications/notifications.component';
import { SharedModule } from '../shared/shared.module';
import { CurriculumViewComponent } from './pages/curriculum-view/curriculum-view.component';


@NgModule({
  declarations: [IndexComponent, InterviewDetailComponent, CurriculumComponent, NotificationsComponent, CurriculumViewComponent],
  imports: [
    CommonModule,
    UserRoutingModule,
    SharedModule
  ]
})
export class UserModule { }
