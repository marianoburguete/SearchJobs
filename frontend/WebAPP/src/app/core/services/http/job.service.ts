import { Injectable } from '@angular/core';
import {
  HttpClient,
  HttpHeaders,
  HttpErrorResponse,
  HttpParams
} from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { searchJobDto } from '../../models/searchJobDto';
import { query } from '@angular/animations';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root',
})
export class JobService {

  prefix = environment.URLAPI + 'jobs';

  constructor(private httpClient: HttpClient, private authService: AuthService) {}

  search(data:searchJobDto) {
    return this.httpClient.post(this.prefix + '/search', data);
  }

  details(job_id) {
    return this.httpClient.get(this.prefix + '/' + job_id);
  }

  application(job_id) {
    let data = {'job_id': job_id}
    return this.httpClient.post(this.prefix + '/application', data, {headers: this.authService.getheaders().headers});
  }

  applicationExists(job_id) {
    let params = new HttpParams().set('job_id', job_id);
    return this.httpClient.get(this.prefix + '/application', {params: params, headers: this.authService.getheaders().headers});
  }
}