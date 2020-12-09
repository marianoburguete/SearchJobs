import { NgModule } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';

import { UserRoutingModule } from './user-routing.module';
import { IndexComponent } from './pages/index/index.component';
import { InterviewDetailComponent } from './pages/interview-detail/interview-detail.component';
import { CurriculumComponent } from './pages/curriculum/curriculum.component';
import { NotificationsComponent } from './pages/notifications/notifications.component';
import { SharedModule } from '../shared/shared.module';
import { CurriculumViewComponent } from './pages/curriculum-view/curriculum-view.component';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { InterviewsListComponent } from './interviews-list/interviews-list.component';
import { ApplicationsListComponent } from './applications-list/applications-list.component';
import { ImageReplacementCurriculumEdit } from '../../core/pipes/image-replacement-curriculum-edit-pipe';


@NgModule({
  declarations: [IndexComponent, InterviewDetailComponent, CurriculumComponent, NotificationsComponent, CurriculumViewComponent, InterviewsListComponent, ApplicationsListComponent, ImageReplacementCurriculumEdit],
  imports: [
    CommonModule,
    UserRoutingModule,
    SharedModule,
    NgxChartsModule
  ],
  providers: [
    DatePipe
  ]
})
export class UserModule { }
