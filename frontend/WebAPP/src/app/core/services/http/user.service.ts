import { Injectable } from '@angular/core';
import {
  HttpClient,
  HttpHeaders,
  HttpErrorResponse,
  HttpParams,
} from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  prefix = environment.URLAPI + 'users';

  constructor(
    private httpClient: HttpClient,
    private authService: AuthService
  ) {}

  searchUsersByEmail(data) {
    return this.httpClient.post(this.prefix + '/a/searchbyemail', data, {headers: this.authService.getheaders().headers});
  }

  getById(data) {
    return this.httpClient.get(this.prefix + '/a/' + data.id, { headers: this.authService.getheaders().headers});
  }
}
