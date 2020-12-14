import { Pipe, PipeTransform } from '@angular/core';
import { AuthService } from '../services/http/auth.service';

@Pipe({name: 'chatMessageClass'})
export class ChatMessageClassPipe implements PipeTransform {
  transform(value): string {
      let authService: AuthService;
      let user = authService.getUser();
    if (user.email === value) {
        return 'chatBox';
    }
    return 'chatBox1';
  }
}