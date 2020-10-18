import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AlertDTO } from 'src/app/core/models/alertDto';
import { InterviewService } from 'src/app/core/services/http/interview.service';
import { SpinnerService } from 'src/app/core/services/spinner.service';
import { UserService } from '../../../core/services/http/user.service';
import { JobService } from '../../../core/services/http/job.service';
import { first } from 'rxjs/operators';

@Component({
  selector: 'app-interviews-create',
  templateUrl: './interviews-create.component.html',
  styleUrls: ['./interviews-create.component.scss']
})
export class InterviewsCreateComponent implements OnInit {

  alert: AlertDTO = {
    show: false,
    msg: null,
    errorCode: null
  }

  userFilter: number = null;
  jobFilter: number = null;
  userEmail: string = null;
  jobTitle: string = null;
  firstMessage: string = null;

  constructor(private interviewService: InterviewService, private userService: UserService, private jobService: JobService,private spinnerService: SpinnerService, private route: ActivatedRoute, private router: Router) { }

  ngOnInit() {
    this.route.queryParamMap.subscribe(params => {
      if (params.get('user') != null) {
        this.userFilter = Number(params.get('user'));
        this.userService.getById({id: this.userFilter}).subscribe(res => {
          this.userEmail = res['user']['email'];
        });
      }
      if (params.get('job') != null) {
        this.jobFilter = Number(params.get('job'));
        this.jobService.details(this.jobFilter).subscribe(res => {
          this.jobTitle = res['results']['title'];
        });
      }
    });
  }

  newInterview() {
    if (this.userFilter != null && this.jobFilter != null && this.firstMessage != null) {
      this.spinnerService.callSpinner();
      const data = {
        user_id: this.userFilter,
        job_id: this.jobFilter,
        text: this.firstMessage
      }
      this.interviewService.add(data).subscribe((res) => {
        this.router.navigate(['/admin/entrevistas', res['result']['id']]);
      },
      (err) => {
        this.alert.show = true;
        //TODO no muestra el msg por alguna razon, arreglar
        this.alert.msg = err.body.msg;
      }).add(() => this.spinnerService.stopSpinner());
    }
    else{
      this.alert.show = true;
      this.alert.msg = 'Todos los campos deben tener datos';
    }
  }

  setUserFilter(u:any) {
    this.userFilter = u.id;
    this.userEmail = u.email;
  }

  setJobFilter(j:any) {
    this.jobFilter = j.id;
    this.jobTitle = j.title;
  }

}
