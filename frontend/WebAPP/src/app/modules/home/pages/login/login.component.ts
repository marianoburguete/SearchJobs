import { Component, OnInit } from '@angular/core';

import { Router } from '@angular/router';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { AuthValidationService } from '../../../../core/services/validators/auth-validation.service';
import { AuthService } from '../../../../core/services/http/auth.service';
import { AlertDTO } from 'src/app/core/models/alertDto';
import { SpinnerService } from '../../../../core/services/spinner.service';
import { finalize } from 'rxjs/operators';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  alert: AlertDTO = {
    show: false,
    msg: null,
    errorCode: null,
  };

  constructor(
    private fb: FormBuilder,
    private _router: Router,
    private _authService: AuthService,
    private loginValidator: AuthValidationService,
    private spinnerService: SpinnerService
  ) {}

  ngOnInit() {
    this.loginForm = this.fb.group({
      email: [
        '',
        {
          validators: [Validators.required, Validators.email],
        },
      ],
      password: [
        '',
        Validators.compose([
          Validators.required,
          this.loginValidator.patternValidator(),
        ]),
      ],
    });
  }

  get registerLoginControl() {
    return this.loginForm.controls;
  }

  get loginValidation() {
    return this.loginForm;
  }

  loginSubmit() {
    if (this.loginForm.valid) {
      this.spinnerService.callSpinner();
      this._authService
        .login(
          this.loginForm.controls['email'].value,
          this.loginForm.controls['password'].value
        )
        .subscribe(
          (res) => {
            let u = res['userSession'];
            localStorage.setItem('userSession', JSON.stringify(u));
            this._authService.user = JSON.parse(
              localStorage.getItem('userSession')
            );
            console.log(this._authService.user.email);
            this._router.navigate(['home']);
          },
          (err) => {
            console.log(err.body.msg);
            this.alert.msg = err.body.msg;
            this.alert.errorCode = 'alert-danger';
            this.alert.show = true;
          }
        )
        .add(() => {
          this.spinnerService.stopSpinner();
        });
    } else {
      let error = 'Los datos deben ser validos';
    }
  }
}
