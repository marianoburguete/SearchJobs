import { Pipe, PipeTransform } from '@angular/core';

@Pipe({name: 'dayOrDays'})
export class DayOrDaysPipe implements PipeTransform {
  transform(value): string {
    let da: any = new Date(value);
    let now: any = new Date();
    value =  Math.floor((now - da) / (1000 * 60 * 60 * 24));

    if (value < '1') {
      return 'Hoy';
    }
    if (value == '1') {
        return 'Hace' + value + ' día';
    } else {
        return 'Hace' + value +  ' días';
    }
  }
}