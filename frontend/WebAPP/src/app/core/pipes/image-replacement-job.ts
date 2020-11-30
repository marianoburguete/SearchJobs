import { Pipe, PipeTransform } from '@angular/core';

@Pipe({name: 'imageReplacementJobDet'})
export class ImageReplacementJob implements PipeTransform {
  transform(value: string): string {
    if (value == null) {
        return 'https://via.placeholder.com/150x150';
    } else {
        return value;
    }
  }
}