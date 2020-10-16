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
export class ApplicationService {
  prefix = environment.URLAPI + 'applications';

  constructor(
    private httpClient: HttpClient,
    private authService: AuthService
  ) {}

  getAll(data) {
    return this.httpClient.post(this.prefix + '/a', data, {
      headers: this.authService.getheaders().headers,
    });
  }

  dismissApplication(data) {
    return this.httpClient.post(this.prefix + '/a/dismiss', data, {headers: this.authService.getheaders().headers});
  }
}
