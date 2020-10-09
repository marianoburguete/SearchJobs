import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';
import { userSessionModel } from '../../models/userSessionModel';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  prefix = environment.URLAPI + 'auth';
  
  user:userSessionModel = null;

  constructor(
    private httpClient: HttpClient
  ) { 
    let us = localStorage.getItem('userSession')
    if (us !== null) {
      this.user = JSON.parse(us);
    }
  }

  login(email, password){
    let data = {'email': email, 'password': password};
    return this.httpClient.post(this.prefix + '/signin', data).pipe(
      catchError(this.handleError)
    );
  }

  register(email, password){
    let data = {'email': email, 'password': password};
    return this.httpClient.post(this.prefix + '/signup', data).pipe(
      catchError(this.handleError)
    )
  }

  emailExists(email){
    let data = {'email': email};
    return this.httpClient.post(this.prefix + '/email', data).pipe(
      catchError(this.handleError)
    );
  }

  isLogged() {
    let userSession = localStorage.getItem('userSession');
    if (userSession) {
      return true;
    }
    else{
      return false;
    }
  }

  getRole() {
    let userSession = localStorage.getItem('userSession');
    if (userSession) {
      userSession = JSON.parse(userSession);
      return userSession['role'];
    }
    else{
      return null;
    }
  }
  
  getUser(): userSessionModel {
    let userSession = localStorage.getItem('userSession');
    if (userSession) {
      let u:userSessionModel = JSON.parse(userSession);
      return u;
    }
    else{
      return null;
    }
  }

  getheaders(){
    let Token = this.getToken();
    if (Token != '') {
      return {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + Token
        })
      };
    } else {
      return {
        headers: new HttpHeaders({})
      };
    }
  }

  private getToken() {
    if (localStorage.getItem("userSession") && localStorage.getItem("userSession") != '') {
        let Session = JSON.parse(localStorage.getItem("userSession"));
        if (Session != null) return Session.access_token;
    }
    return '';
  }

  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
        console.error('An error occurred:', error.error.message);
    } else {
        console.error(
            `Backend returned code ${error.status}, ` +
            `body was: ${error.error}`);
    }
    return throwError(
        {
            code: error.status,
            body: error.error
        }
    );
}
}
