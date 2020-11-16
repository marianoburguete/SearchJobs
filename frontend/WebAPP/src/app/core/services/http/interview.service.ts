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
  providedIn: 'root'
})
export class InterviewService {

  prefix = environment.URLAPI + 'interviews';

  constructor(
    private httpClient: HttpClient,
    private authService: AuthService
  ) { }

  getAll(data) {
    return this.httpClient.post(this.prefix + '/a/getall', data, {headers: this.authService.getheaders().headers});
  }
  
  getAllUser(data) {
    data.user = this.authService.getUser().id;
    return this.httpClient.post(this.prefix + '/user/' + this.authService.getUser().id, data, {headers: this.authService.getheaders().headers});
  }
  
  get(data) {
    return this.httpClient.get(this.prefix + '/a/' + data.id, {headers: this.authService.getheaders().headers});
  }

  add(data) {
    return this.httpClient.post(this.prefix + '/a', data, {headers: this.authService.getheaders().headers});
  }

  put(data) {
    return this.httpClient.put(this.prefix + '/a/' + data.id, data, {headers: this.authService.getheaders().headers});
  }

  addMessage(data) {
    return this.httpClient.post(this.prefix + '/' + data.id + '/message', data, {headers: this.authService.getheaders().headers});
  }

  getInterviewForUser(data) {
    return this.httpClient.get(this.prefix + '/' + data.id, {headers: this.authService.getheaders().headers});
  }
}
