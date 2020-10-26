import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AlertDTO } from 'src/app/core/models/alertDto';
import { SpinnerService } from 'src/app/core/services/spinner.service';
import { CompanyService } from 'src/app/core/services/http/company.service';

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.scss']
})
export class IndexComponent implements OnInit {

  alert: AlertDTO = {
    show: false,
    msg: null,
    errorCode: null
  }
  companiesList: any;
  pageFilter = 1;
  statusFilter: string = null;
  messagesStatusFilter: boolean = null;

  currentPage = 1;
  nextPage: number = null;
  previousPage: number = null;

  constructor(private companyService: CompanyService, private spinnerService: SpinnerService, private route: ActivatedRoute, private router: Router) { }

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

      this.companyService.getAll(data).subscribe((res) => {
        this.companiesList = res['results'];
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

  previousPageLink() {
    let params:any = {
      status: this.statusFilter,
      page: this.previousPage
    };
    this.router.navigate(['/admin/entrevistas'], {queryParams: params});
  }
  
  nextPageLink() {
    let params:any = {
      status: this.statusFilter,
      page: this.nextPage
    };
    this.router.navigate(['/admin/entrevistas'], {queryParams: params});
  }

}
