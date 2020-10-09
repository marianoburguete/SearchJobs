import { Component, OnInit } from '@angular/core';

import { Router } from '@angular/router';
import { FormGroup, FormBuilder, Validators, FormControlName } from '@angular/forms';
import { AuthValidationService } from '../../../../core/services/validators/auth-validation.service';
import { AuthService } from '../../../../core/services/http/auth.service';
import { SpinnerService } from '../../../../core/services/spinner.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

  registerForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private _router: Router,
    private _authService: AuthService,
    private loginValidator: AuthValidationService,
    private spinerService: SpinnerService
  ) { }

  ngOnInit(): void {
    this.registerForm = this.fb.group({
      email: ['', {
        validators: [Validators.required, Validators.email],
        asyncValidators: AuthValidationService.emailValidator(this._authService),
        updateOn: 'blur'
      }],
      password: ['', Validators.compose([Validators.required, this.loginValidator.patternValidator()])],
      passwordConfirm: ['', Validators.required]
    },
    {
      validator: this.loginValidator.MatchPassword('password', 'passwordConfirm')
    });
  }

  get registerLoginControl() {
    return this.registerForm.controls;
  }

  get loginValidation(){
    return this.registerForm;
  }

  registerSubmit() {
    if(this.registerForm.valid){
      this.spinerService.callSpinner();
      this._authService.register(this.registerForm.controls['email'].value, this.registerForm.controls['password'].value).subscribe(
        (res) => {
          this._router.navigate(['login']);
        },
        err => {
          console.log(err.body.msg);
        }
      ).add(() => {
        this.spinerService.stopSpinner();
      });
    }
    else{
      let error = 'Los datos deben ser validos';
      console.log(error);
    }
  }

}
