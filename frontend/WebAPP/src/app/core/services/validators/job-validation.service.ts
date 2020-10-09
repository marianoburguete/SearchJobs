import { Injectable } from '@angular/core';
import { AbstractControl } from '@angular/forms';
import { map } from 'rxjs/operators';
import { JobService } from '../http/job.service';

@Injectable({
  providedIn: 'root'
})
export class JobValidationService {

  constructor() { }

  static emailValidator(jobService: JobService) {
    return (control: AbstractControl) => {
      const value = control.value;
      return jobService.search(value).pipe(
        map((response) => {
          if (response['email'] === true) {
            return { emailNotAvailable: true };
          }
          return null;
        })
      );
    };
  }
}
