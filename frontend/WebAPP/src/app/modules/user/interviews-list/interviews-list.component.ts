import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AlertDTO } from 'src/app/core/models/alertDto';
import { InterviewService } from 'src/app/core/services/http/interview.service';
import { SpinnerService } from 'src/app/core/services/spinner.service';

@Component({
  selector: 'app-interviews-list',
  templateUrl: './interviews-list.component.html',
  styleUrls: ['./interviews-list.component.scss'],
})
export class InterviewsListComponent implements OnInit {
  alert: AlertDTO = {
    show: false,
    msg: null,
    errorCode: null,
  };
  interviewsList: any;
  jobFilter: number = null;
  pageFilter = 1;
  jobTitle: string = null;
  statusFilter: string = null;
  messagesStatusFilter: boolean = null;

  currentPage = 1;
  nextPage: number = null;
  previousPage: number = null;

  constructor(
    private interviewService: InterviewService,
    private spinnerService: SpinnerService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit() {
    this.spinnerService.callSpinner();
    this.route.queryParamMap.subscribe((param) => {
      let data: any = {
        page: this.pageFilter,
        per_page: 10,
        status: 'created'
      };

      if (param.get('page') != null) {
        this.pageFilter = Number(param.get('page'));
        data.page = this.pageFilter;
      }
      if (param.get('status') != null) {
        this.statusFilter = param.get('status');
        data.status = this.statusFilter;
      }
      else{
        this.statusFilter = 'created';
      }
      if (param.get('job') != null) {
        this.jobFilter = Number(param.get('job'));
        data.job = this.jobFilter;
      }
      if (param.get('unread') != null) {
        this.messagesStatusFilter = param.get('unread') === 'true';
        console.log(this.messagesStatusFilter);
        data.unread = this.messagesStatusFilter;
      }
      this.interviewService.getAllUser(data).subscribe((res) => {
        this.interviewsList = res['results'];
        this.currentPage = res['currentPage'];
        this.previousPage = res['previousPage'];
        this.nextPage = res['nextPage'];
      },
      (err) => {
        this.alert.show = true;
        this.alert.msg = err.error.msg;
        this.alert.errorCode = 'alert-danger';
      }).add(() => this.spinnerService.stopSpinner());
    });
  }

  setJobFilter(j:any) {
    this.jobFilter = j.id;
    this.jobTitle = j.title;
  }

  filter() {
    let params:any = {
      status: this.statusFilter
    };
    if (this.jobFilter != null) {
      params.job = this.jobFilter;
    }
    if (this.messagesStatusFilter != null) {
      params.unread = this.messagesStatusFilter;
    }
    this.router.navigate(['/usuario/entrevistas'], {queryParams: params});
  }

  previousPageLink() {
    let params:any = {
      status: this.statusFilter,
      page: this.previousPage
    };
    if (this.jobFilter != null) {
      params.job = this.jobFilter;
    }
    this.router.navigate(['/usuario/entrevistas'], {queryParams: params});
  }
  
  nextPageLink() {
    let params:any = {
      status: this.statusFilter,
      page: this.nextPage
    };
    if (this.jobFilter != null) {
      params.job = this.jobFilter;
    }
    this.router.navigate(['/usuario/entrevistas'], {queryParams: params});
  }

  lala() {
    console.log(this.messagesStatusFilter);
  }
}
