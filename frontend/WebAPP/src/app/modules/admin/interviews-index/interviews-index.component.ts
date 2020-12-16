import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AlertDTO } from 'src/app/core/models/alertDto';
import { SpinnerService } from 'src/app/core/services/spinner.service';
import { InterviewService } from '../../../core/services/http/interview.service';

@Component({
  selector: 'app-interviews-index',
  templateUrl: './interviews-index.component.html',
  styleUrls: ['./interviews-index.component.scss']
})
export class InterviewsIndexComponent implements OnInit {

  alert: AlertDTO = {
    show: false,
    msg: null,
    errorCode: null
  }
  interviewsList: any;
  userFilter: number = null;
  jobFilter: number = null;
  pageFilter = 1;
  userEmail: string = null;
  jobTitle: string = null;
  statusFilter: string = null;
  messagesStatusFilter: boolean = null;
  orderFilter = 'any';
  orderDateInterviewFilter = 'any';

  currentPage = 1;
  nextPage: number = null;
  previousPage: number = null;

  constructor(private interviewService: InterviewService, private spinnerService: SpinnerService, private route: ActivatedRoute, private router: Router) { }

  ngOnInit() {
    this.spinnerService.callSpinner();
    this.route.queryParamMap.subscribe((param) => {
      let data: any = {
        page: this.pageFilter,
        per_page: 10,
        status: 'created',
        order: this.orderFilter,
        orderByInterviewDate: this.orderDateInterviewFilter
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
      if (param.get('order') != null) {
        this.orderFilter = param.get('order');
        data.order = this.orderFilter;
      }
      else {
        if (param.get('orderInterviewDate') != null) {
          this.orderDateInterviewFilter = param.get('orderInterviewDate');
          data.orderInterviewDate = this.orderDateInterviewFilter;
        }
      }
      if (data.order === 'any' && data.orderInterviewDate === 'any') {
        data.order = 'desc'
      }
      if(param.get('user') != null){
        this.userFilter = Number(param.get('user'));
        data.user = this.userFilter;
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

      this.interviewService.getAll(data).subscribe((res) => {
        this.interviewsList = res['results'];
        this.currentPage = res['currentPage'];
        this.previousPage = res['previousPage'];
        this.nextPage = res['nextPage'];
      },
      (err) => {
        this.alert.show = true;
        this.alert.msg = err.msg;
      }).add(() => this.spinnerService.stopSpinner());
    });
  }

  setUserFilter(u:any) {
    this.userFilter = u.id;
    this.userEmail = u.email;
  }

  setJobFilter(j:any) {
    this.jobFilter = j.id;
    this.jobTitle = j.title;
  }

  filter() {
    let params:any = {
      status: this.statusFilter,
      order: this.orderFilter,
      orderByInterviewDate: this.orderDateInterviewFilter
    };
    if (this.userFilter != null) {
      params.user = this.userFilter;
    }
    if (this.jobFilter != null) {
      params.job = this.jobFilter;
    }
    if (this.messagesStatusFilter != null) {
      params.unread = this.messagesStatusFilter;
    }
    this.router.navigate(['/admin/entrevistas'], {queryParams: params});
  }

  previousPageLink() {
    let params:any = {
      status: this.statusFilter,
      order: this.orderFilter,
      page: this.previousPage
    };
    if (this.userFilter != null) {
      params.user = this.userFilter;
    }
    if (this.jobFilter != null) {
      params.job = this.jobFilter;
    }
    this.router.navigate(['/admin/entrevistas'], {queryParams: params});
  }
  
  nextPageLink() {
    let params:any = {
      status: this.statusFilter,
      order: this.orderFilter,
      page: this.nextPage
    };
    if (this.userFilter != null) {
      params.user = this.userFilter;
    }
    if (this.jobFilter != null) {
      params.job = this.jobFilter;
    }
    this.router.navigate(['/admin/entrevistas'], {queryParams: params});
  }

  lala() {
    console.log(this.messagesStatusFilter);
  }

}
