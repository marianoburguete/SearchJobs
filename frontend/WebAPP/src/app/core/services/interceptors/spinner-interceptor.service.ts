import { HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { SpinnerService } from '../spinner.service';
import { Observable } from 'rxjs';
import { finalize } from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class SpinnerInterceptorService implements HttpInterceptor {

  constructor(private spinnerService: SpinnerService) { }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<any> {
    this.spinnerService.callSpinner();
    return next.handle(req).pipe(
      finalize( () => this.spinnerService.stopSpinner())
    );
  }
}
