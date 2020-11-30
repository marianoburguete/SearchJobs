import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'salaryFormatPipe' })
export class SalaryFormatPipe implements PipeTransform {
  transform(value): string {
    if (value != null) {
      return value;
    } else {
      return 'No especificado';
    }
  }
}

@Pipe({ name: 'workdayFormatPipe' })
export class WorkdayFormatPipe implements PipeTransform {
  transform(value): string {
    if (value != null) {
      if (value === 'fulltime') {
        return 'Tiempo completo';
      } else if (value === 'parttime') {
        return 'Medio tiempo';
      }
    }
    return 'No especificado';
  }
}

@Pipe({ name: 'localizationFormatPipe' })
export class LocalizationFormatPipe implements PipeTransform {
  transform(value): string {
    if (value != null) {
        if (value === 'remote') {
            return 'Remoto';
        }
        return value;
    }
    return 'No especificado';
  }
}

@Pipe({ name: 'contractFormatPipe' })
export class ContractFormatPipe implements PipeTransform {
  transform(value): string {
    if (value != null) {
        if (value === 'defined') {
            return 'Tiempo definido';
        } else if (value === 'undefined') {
            return 'Tiempo indefinido';
        }
    }
    return 'No especificado';
  }
}
