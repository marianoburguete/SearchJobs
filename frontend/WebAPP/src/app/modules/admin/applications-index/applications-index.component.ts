import { Component, OnInit } from '@angular/core';
import { ErrorStateMatcher } from '@angular/material/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AlertDTO } from 'src/app/core/models/alertDto';
import { SpinnerService } from 'src/app/core/services/spinner.service';
import { ApplicationService } from '../../../core/services/http/application.service';

@Component({
  selector: 'app-applications-index',
  templateUrl: './applications-index.component.html',
  styleUrls: ['./applications-index.component.scss']
})
export class ApplicationsIndexComponent implements OnInit {

  alert: AlertDTO = {
    show: false,
    msg: null,
    errorCode: null
  }
  applicationsList: any;
  userFilter: number = null;
  jobFilter: number = null;
  pageFilter = 1;
  userEmail: string = null;
  jobTitle: string = null;
  statusFilter: string = null;
  orderFilter = 'desc';

  statusFilterTemp: string = null;

  currentPage = 1;
  nextPage: number = null;
  previousPage: number = null;

  constructor(private applicationService: ApplicationService, private spinnerService: SpinnerService, private route: ActivatedRoute, private router: Router) { }

  ngOnInit() {
    this.spinnerService.callSpinner();
    this.route.queryParamMap.subscribe((param) => {
      let data: any = {
        page: this.pageFilter,
        per_page: 10,
        status: 'created',
        order: this.orderFilter
      };

      if (param.get('page') != null) {
        this.pageFilter = Number(param.get('page'));
        data.page = this.pageFilter;
      }
      if (param.get('status') != null) {
        this.statusFilter = param.get('status');
        data.status = this.statusFilter;
        this.statusFilterTemp = this.statusFilter;
      }
      else{
        this.statusFilter = 'created';
      }
      if (param.get('order') != null) {
        this.orderFilter = param.get('order');
        data.order = this.orderFilter;
      }
      if(param.get('user') != null){
        this.userFilter = Number(param.get('user'));
        data.user = this.userFilter;
      }
      if (param.get('job') != null) {
        this.jobFilter = Number(param.get('job'));
        data.job = this.jobFilter;
      }

      this.applicationService.getAll(data).subscribe((res) => {
        this.applicationsList = res['results'];
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

  dismissApplication(id) {
    this.spinnerService.callSpinner();
    this.applicationService.dismissApplication({id: id}).subscribe((res) => {
      this.alert.show = true;
      this.alert.msg = 'Postulacion descartada.';
      this.alert.errorCode = 200;
    },(err) => {
      this.alert.show = true;
      this.alert.msg = err.msg;
      this.alert.errorCode = 500;
    }).add(() => this.spinnerService.stopSpinner());
  }

  filter() {
    let params:any = {
      status: this.statusFilter,
      order: this.orderFilter,
      page: 1
    };
    if (this.userFilter != null) {
      params.user = this.userFilter;
    }
    if (this.jobFilter != null) {
      params.job = this.jobFilter;
    }
    this.router.navigate(['/admin/postulaciones'], {queryParams: params});
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
    this.router.navigate(['/admin/postulaciones'], {queryParams: params});
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
    this.router.navigate(['/admin/postulaciones'], {queryParams: params});
  }
}
