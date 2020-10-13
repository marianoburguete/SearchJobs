import { Pipe, PipeTransform } from '@angular/core';

@Pipe({name: 'remoteString'})
export class RemoteLocationPipe implements PipeTransform {
  transform(value: string): string {
    if (value === 'remote') {
        return 'Remoto';
    } else {
        return value;
    }
  }
}