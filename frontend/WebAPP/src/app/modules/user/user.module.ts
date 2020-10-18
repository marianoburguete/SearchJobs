import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { UserRoutingModule } from './user-routing.module';
import { IndexComponent } from './pages/index/index.component';
import { InterviewDetailComponent } from './pages/interview-detail/interview-detail.component';
import { CurriculumComponent } from './pages/curriculum/curriculum.component';
import { NotificationsComponent } from './pages/notifications/notifications.component';
import { SharedModule } from '../shared/shared.module';
import { MessageStatusPipe } from '../../core/pipes/interview-pipe';


@NgModule({
  declarations: [IndexComponent, InterviewDetailComponent, CurriculumComponent, NotificationsComponent],
  imports: [
    CommonModule,
    UserRoutingModule,
    SharedModule
  ]
})
export class UserModule { }
