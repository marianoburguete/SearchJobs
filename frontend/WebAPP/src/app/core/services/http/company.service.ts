import { Injectable } from '@angular/core';
import {
  HttpClient
} from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { AuthService } from './auth.service';


@Injectable({
  providedIn: 'root'
})
export class CompanyService {

  prefix = environment.URLAPI + 'company';

  constructor(
    private httpClient: HttpClient,
    private authService: AuthService
  ) { }

  getAll(data) {
    return this.httpClient.post(this.prefix + '/a/getall', data, {headers: this.authService.getheaders().headers});
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

}
