import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AlertDTO } from 'src/app/core/models/alertDto';
import { cv } from 'src/app/core/models/cv';
import { UserService } from '../../../core/services/http/user.service';
import { SpinnerService } from '../../../core/services/spinner.service';

@Component({
  selector: 'app-user-details',
  templateUrl: './user-details.component.html',
  styleUrls: ['./user-details.component.scss']
})
export class UserDetailsComponent implements OnInit {

  alert: AlertDTO = {
    show: false,
    msg: null,
    errorCode: null,
  };

  userId: number = null;
  curriculum: cv = {
    education: [],
    workexperience: [],
    languages: [],
    categories: []
  };

  constructor(
    private userService: UserService,
    private spinnerService: SpinnerService,
    private route: ActivatedRoute
  ) { }

  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      this.userId = Number(params.get('id'));
      this.spinnerService.callSpinner();
      this.userService.getCurriculumAdmin(this.userId).subscribe(res => {
        this.curriculum = res['results'];
      },
      err => {
        this.alert.show = true;
        this.alert.msg = err.error.msg;
        this.alert.errorCode = 'alert-danger';
      }).add(() => this.spinnerService.stopSpinner());
    });
  }

}
