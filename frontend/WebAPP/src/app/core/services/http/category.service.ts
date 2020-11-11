import { Injectable } from '@angular/core';
import {
  HttpClient
} from '@angular/common/http';
import { environment } from 'src/environments/environment';


@Injectable({
  providedIn: 'root'
})
export class CategoryService {

  prefix = environment.URLAPI + 'categories';

  constructor(
    private httpClient: HttpClient
  ) { }

  getAll() {
    return this.httpClient.get(this.prefix);
  }
}