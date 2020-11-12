import { Pipe, PipeTransform } from '@angular/core';

@Pipe({name: 'noInfoDetailsString'})
export class NoInfoDetailsPipe implements PipeTransform {
  transform(value: string): string {
    if (value !== null) {
        return 'Esta empresa no tiene descripcion.';
    } else {
        return value;
    }
  }
}