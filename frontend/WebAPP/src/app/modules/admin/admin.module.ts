import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AdminRoutingModule } from './admin-routing.module';
import { IndexComponent } from './index/index.component';
import { ApplicationsIndexComponent } from './applications-index/applications-index.component';
import { SharedModule } from '../shared/shared.module';
import { FormsModule } from '@angular/forms';
import { UserDetailsComponent } from './user-details/user-details.component';
import { InterviewsIndexComponent } from './interviews-index/interviews-index.component';
import { InterviewsCreateComponent } from './interviews-create/interviews-create.component';
import { InterviewsDetailsComponent } from './interviews-details/interviews-details.component';
import { InterviewStatusPipe, MessageStatusPipe } from '../../core/pipes/interview-pipe';


@NgModule({
  declarations: [IndexComponent, ApplicationsIndexComponent, UserDetailsComponent, InterviewsIndexComponent, InterviewsCreateComponent, InterviewsDetailsComponent],
  imports: [
    CommonModule,
    AdminRoutingModule,
    SharedModule,
    FormsModule
  ]
})
export class AdminModule { }
