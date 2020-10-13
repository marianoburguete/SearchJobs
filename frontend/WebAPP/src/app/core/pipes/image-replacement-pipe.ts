import { Pipe, PipeTransform } from '@angular/core';

@Pipe({name: 'imageReplacement'})
export class ImageReplacementPipe implements PipeTransform {
  transform(value: string): string {
    if (value == null) {
        return 'https://via.placeholder.com/150x150';
    } else {
        return value;
    }
  }
}