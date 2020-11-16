import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AlertDTO } from 'src/app/core/models/alertDto';
import { CompanyService } from 'src/app/core/services/http/company.service';
import { JobService } from 'src/app/core/services/http/job.service';
import { searchJobDto } from '../../../../core/models/searchJobDto';
import { SpinnerService } from 'src/app/core/services/spinner.service';

@Component({
  selector: 'app-details',
  templateUrl: './details.component.html',
  styleUrls: ['./details.component.scss']
})
export class DetailsComponent implements OnInit {
  pageNumber = 1;
  nextPageNumber = null;
  previousPageNumber = null;
  lastPageNumber = null;
  totalResults = 0;

  alert: AlertDTO = {
    show: false,
    msg: null,
    errorCode: null,
  };

  company: any = null;
  jobs: any = null;
  mensaje: any = null;
  rating : any = null;

  constructor(
    private companyService: CompanyService,
    private jobService : JobService,
    private spinnerService: SpinnerService,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    let id = null;
    let pagina = null;
    this.spinnerService.callSpinner();
    this.route.queryParamMap.subscribe((params) => {
      id = params.get('id');
      pagina = params.get('page');
      this.companyService.details(id).subscribe((res) => {
        this.company = res['results'];
      })
    });
    let data: searchJobDto;
    data = {
      page: pagina,
      per_page: 3,
      company_id: id
    };
    this.route.queryParamMap.subscribe((params) =>{
      this.jobService.byCompany(data).subscribe((res) => {
        this.jobs = res['results'];
        this.makeQueryStrings(res);
      }).add(() => {this.spinnerService.stopSpinner()});
    });
  }

  addRating() {
    if (this.mensaje != null && this.mensaje !== '' && this.rating != null && this.rating !== '') {
      this.spinnerService.callSpinner();
      const data  = {
        id: this.company.id,
        description: this.mensaje,
        score: this.rating
      };
      this.companyService.addRating(data).subscribe(res => {
        this.alert.errorCode = 'alert-primary';
        this.alert.show = true;
        this.alert.msg = 'Rating enviado';
        this.company.ratings = res['results'];
        this.mensaje = null;
        this.rating = null;
      }, err => {
        this.alert.errorCode = 'alert-danger';
          this.alert.show = true;
          this.alert.msg = err.error.msg;
      }).add(() => this.spinnerService.stopSpinner());
    }
  }

  makeQueryStrings(res) {
    this.pageNumber = res.currentPage;
    this.previousPageNumber = res.previousPage;
    this.nextPageNumber = res.nextPage;
    this.lastPageNumber = res.totalPages;
    this.totalResults = res.totalResults;
  }

}
