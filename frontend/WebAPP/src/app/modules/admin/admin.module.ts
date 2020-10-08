import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AdminRoutingModule } from './admin-routing.module';
import { AdminComponent } from './admin.component';
import { IndexComponent } from './index/index.component';
import { ApplicationsIndexComponent } from './applications-index/applications-index.component';


@NgModule({
  declarations: [AdminComponent, IndexComponent, ApplicationsIndexComponent],
  imports: [
    CommonModule,
    AdminRoutingModule
  ]
})
export class AdminModule { }
