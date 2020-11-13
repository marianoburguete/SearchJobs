import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AlertDTO } from 'src/app/core/models/alertDto';
import { cv } from 'src/app/core/models/cv';
import { UserService } from 'src/app/core/services/http/user.service';
import { SpinnerService } from 'src/app/core/services/spinner.service';

@Component({
  selector: 'app-curriculum-view',
  templateUrl: './curriculum-view.component.html',
  styleUrls: ['./curriculum-view.component.scss']
})
export class CurriculumViewComponent implements OnInit {

  alert: AlertDTO = {
    show: false,
    msg: null,
    errorCode: null,
  };

  curriculum: cv = {
    education: [],
    workexperience: [],
    languages: [],
    categories: []
  };

  constructor(
    private userService: UserService,
    private spinnerService: SpinnerService,
    private route: ActivatedRoute,
    private router: Router
  ) { }

  ngOnInit() {
    this.spinnerService.callSpinner();
    this.userService.getCurriculum().subscribe(res => {
      this.curriculum = res['results'];
    },
    err => {
      this.alert.show = true;
      this.alert.msg = err.error.msg;
      this.alert.errorCode = 'alert-danger';
    }).add(() => this.spinnerService.stopSpinner());
  }

}
