import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'interviewStatusPipe' })
export class InterviewStatusPipe implements PipeTransform {
  transform(value): string {
    if (value != null) {
      switch (value) {
          case 'created':
              return 'En negociación';
          case 'confirmed':
              return 'Fijada';
          case 'finished':
              return 'Finalizada';
          case 'cancelled':
              return 'Cancelada';
      
          default:
            return 'No especificado';
      }
    } else {
      return 'No especificado';
    }
  }
}

@Pipe({ name: 'messageStatusPipe' })
export class MessageStatusPipe implements PipeTransform {
  transform(value): string {
    if (value != null) {
      switch (value) {
          case 'readed':
              return 'Leído';
          case 'unread':
              return 'No leído';
      
          default:
            return 'No especificado';
      }
    } else {
      return 'No especificado';
    }
  }
}
