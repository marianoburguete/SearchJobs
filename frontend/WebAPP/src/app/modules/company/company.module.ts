import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CompanyRoutingModule } from './company-routing.module';
import { IndexComponent } from './pages/index/index.component';
import { DetailsComponent } from './pages/details/details.component';
import { SharedModule } from '../shared/shared.module';
import { ImageReplacementCompany } from 'src/app/core/pipes/image-replacement-company';
import { NoInfoPipe } from 'src/app/core/pipes/no-info-pipe';
import { NoInfoDetailsPipe } from 'src/app/core/pipes/no-info-details-pipe';
import { ReactiveFormsModule } from '@angular/forms';
import { RatingModule } from 'ng-starrating';

@NgModule({
  declarations: [IndexComponent, DetailsComponent, ImageReplacementCompany, NoInfoPipe, NoInfoDetailsPipe],
  imports: [
    CommonModule,
    CompanyRoutingModule,
    SharedModule,
    ReactiveFormsModule,
    RatingModule
  ]
})
export class CompanyModule { }
