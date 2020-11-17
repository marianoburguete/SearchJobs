import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CompanyRoutingModule } from './company-routing.module';
import { IndexComponent } from './pages/index/index.component';
import { DetailsComponent } from './pages/details/details.component';
import { SharedModule } from '../shared/shared.module';
import { ImageReplacementCompany } from 'src/app/core/pipes/image-replacement-company';
import { ImageReplacementCompanyDetails } from 'src/app/core/pipes/image-replacement-company-details';
import { NoInfoPipe } from 'src/app/core/pipes/no-info-pipe';
import { NoInfoDetailsPipe } from 'src/app/core/pipes/no-info-details-pipe';
import { ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [IndexComponent, DetailsComponent, ImageReplacementCompany, ImageReplacementCompanyDetails, NoInfoPipe, NoInfoDetailsPipe],
  imports: [
    CommonModule,
    CompanyRoutingModule,
    SharedModule,
    ReactiveFormsModule
  ]
})
export class CompanyModule { }
