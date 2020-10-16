import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { JobRoutingModule } from './job-routing.module';
import { IndexComponent } from './pages/index/index.component';
import { DetailComponent } from './pages/detail/detail.component';
import { SharedModule } from '../shared/shared.module';
import { ReactiveFormsModule } from '@angular/forms';
import { Message } from '@angular/compiler/src/i18n/i18n_ast';

import { RemoteLocationPipe } from '../../core/pipes/remote-location-pipe';
import { DayOrDaysPipe } from '../../core/pipes/day-or-days-pipe';
import { ImageReplacementPipe } from '../../core/pipes/image-replacement-pipe';
import { SalaryFormatPipe, WorkdayFormatPipe, LocalizationFormatPipe, ContractFormatPipe } from '../../core/pipes/requirements-format-pipe';

@NgModule({
  declarations: [IndexComponent, DetailComponent, RemoteLocationPipe, DayOrDaysPipe, ImageReplacementPipe, SalaryFormatPipe, WorkdayFormatPipe, LocalizationFormatPipe, ContractFormatPipe],
  imports: [
    CommonModule,
    JobRoutingModule,
    SharedModule,
    ReactiveFormsModule,
  ]
})
export class JobModule { }
