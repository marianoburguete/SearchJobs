import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { JobService } from '../../../../core/services/http/job.service';
import { JobDetails } from '../../../../core/models/jobDetails';
import { AuthService } from '../../../../core/services/http/auth.service';
import { AlertDTO } from '../../../../core/models/alertDto';
import { SpinnerService } from '../../../../core/services/spinner.service';

@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.scss']
})
export class DetailComponent implements OnInit {

  jobDetails:JobDetails;
  userApplication = false;
  alert: AlertDTO = {
    show: false,
    msg: null,
    errorCode: null
  }

  constructor(
    private jobService: JobService,
    private route: ActivatedRoute,
    public authService: AuthService,
    private spinnerService: SpinnerService
  ) { }

  ngOnInit() {
    this.spinnerService.callSpinner();
    let job_id = null;
    this.route.queryParamMap.subscribe((params) => {
      job_id = params.get('id');
      this.jobService.details(params.get('id')).subscribe((res) => {
        this.jobDetails = res['results'];
        this.jobService.applicationExists(params.get('id')).subscribe((res) => {
          this.userApplication = res['results'];
        }).add(() => {this.spinnerService.stopSpinner()});
      });
    });
  }

  application() {
    this.jobService.application(this.jobDetails.id).subscribe((res) => {
      this.userApplication = true;
    }, (err) => {
      this.alert.show = true;
      this.alert.msg = err.msg;
    });
  }
}
