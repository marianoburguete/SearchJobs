import { Pipe, PipeTransform } from '@angular/core';

@Pipe({name: 'jobDescription'})
export class JobDescription implements PipeTransform {
  transform(value: string): string {
    let text = value.split('.');
    let returnT = '';
    text.forEach(x => {
        returnT += '<br>' + x;
    });
    console.log(returnT);
    return returnT;
  }
}