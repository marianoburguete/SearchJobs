import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { JobRoutingModule } from './job-routing.module';
import { IndexComponent } from './pages/index/index.component';
import { DetailComponent } from './pages/detail/detail.component';
import { SharedModule } from '../shared/shared.module';
import { ReactiveFormsModule } from '@angular/forms';
import { Message } from '@angular/compiler/src/i18n/i18n_ast';

@NgModule({
  declarations: [IndexComponent, DetailComponent],
  imports: [
    CommonModule,
    JobRoutingModule,
    SharedModule,
    ReactiveFormsModule,
  ]
})
export class JobModule { }
