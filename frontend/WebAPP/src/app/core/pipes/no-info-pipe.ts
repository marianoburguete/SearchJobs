import { Pipe, PipeTransform } from '@angular/core';

@Pipe({name: 'noInfoString'})
export class NoInfoPipe implements PipeTransform {
  transform(value: string): string {
    if (value !== null) {
        return '';
    } else {
        return value;
    }
  }
}