import { Pipe, PipeTransform } from '@angular/core';

@Pipe({name: 'imageReplacementCompanyDetails'})
export class ImageReplacementCompanyDetails implements PipeTransform {
  transform(value: string): string {
    if (value == null) {
        return 'http://localhost:4200/assets/images/company-placeholder.png';
    } else {
        return value;
    }
  }
}