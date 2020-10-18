import { Injectable } from '@angular/core';
import {
  HttpClient,
  HttpHeaders,
  HttpErrorResponse,
  HttpParams
} from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { searchJobDto } from '../../models/searchJobDto';
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
    return this.httpClient.post(environment.URLAPI + 'application', data, {headers: this.authService.getheaders().headers});
  }

  applicationExists(job_id) {
    let params = new HttpParams().set('job_id', job_id);
    return this.httpClient.get(environment.URLAPI + 'application', {params: params, headers: this.authService.getheaders().headers});
  }

  searchJobByTitle(data) {
    return this.httpClient.post(this.prefix + '/a/searchbytitle', data, {headers: this.authService.getheaders().headers});
  }
}