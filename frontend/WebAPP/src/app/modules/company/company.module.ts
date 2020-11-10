import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CompanyRoutingModule } from './company-routing.module';
import { IndexComponente } from './pages/index/index.component';
import { DetailsComponent } from './pages/details/details.component';
import { SharedModule } from '../shared/shared.module';
import { ImageReplacementCompany } from 'src/app/core/pipes/image-replacement-company';

@NgModule({
  declarations: [IndexComponente, DetailsComponent, ImageReplacementCompany],
  imports: [
    CommonModule,
    CompanyRoutingModule,
    SharedModule
  ]
})
export class CompanyModule { }
