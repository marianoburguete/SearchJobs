import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from "@angular/common/http";

// Angular Material
import { MatButtonModule } from '@angular/material/button';
import { MatMenuModule } from '@angular/material/menu';
import { MatCardModule } from '@angular/material/card';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';

import { FormsModule } from '@angular/forms';
import { FlexLayoutModule } from '@angular/flex-layout';
import { NgxSpinnerModule } from 'ngx-spinner';
import { MessageAlertComponent } from '../../core/components/message-alert/message-alert.component';
import { ListUsersModalComponent } from '../../core/components/list-users-modal/list-users-modal.component';
import { RouterModule } from '@angular/router';
import { ListJobsModalComponent } from '../../core/components/list-jobs-modal/list-jobs-modal.component';
import { MessageStatusPipe, InterviewStatusPipe } from '../../core/pipes/interview-pipe';
import { DayOrDaysPipe } from '../../core/pipes/day-or-days-pipe';
import { CategoriesNamesPipe } from '../../core/pipes/categories-pipe';



@NgModule({
  declarations: [
    MessageAlertComponent,
    ListUsersModalComponent,
    ListJobsModalComponent,
    MessageStatusPipe,
    InterviewStatusPipe,
    DayOrDaysPipe,
    CategoriesNamesPipe
  ],
  imports: [
    CommonModule,
    HttpClientModule,
    RouterModule
  ],
  exports: [
    MatButtonModule,
    MatMenuModule,
    MatCardModule,
    MatToolbarModule,
    FlexLayoutModule,
    MatSlideToggleModule,
    FormsModule,
    MatSidenavModule,
    MatFormFieldModule,
    MatSelectModule,
    NgxSpinnerModule,
    MessageAlertComponent,
    ListUsersModalComponent,
    ListJobsModalComponent,
    MessageStatusPipe,
    InterviewStatusPipe,
    DayOrDaysPipe,
    CategoriesNamesPipe
  ]
})
export class SharedModule { }
