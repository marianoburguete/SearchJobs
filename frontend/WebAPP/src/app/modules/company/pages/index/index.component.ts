import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { SpinnerService } from 'src/app/core/services/spinner.service';
import { CompanyService } from 'src/app/core/services/http/company.service';
import { companyDto } from 'src/app/core/models/companyDto';

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.scss']
})
export class IndexComponente implements OnInit {
  lastResponse: any = {};
  pageNumber = 1;
  nextPageNumber = null;
  previousPageNumber = null;
  lastPageNumber = null;
  totalResults = 0;

  constructor(
    private _CompanyService: CompanyService,
    private route: ActivatedRoute,
    private spinnerService: SpinnerService
  ) {}

  ngOnInit() {
    this.route.queryParamMap.subscribe((params) => {
      if (params.get('page') != null) {
        this.pageNumber = Number(params.get('page'));
        if (this.pageNumber < 1) {
          this.pageNumber = 1;
        }
      }
      this.searchSubmit();
    });
  }

  searchSubmit() {
    this.spinnerService.callSpinner();
    let data: companyDto;
    data = {
      page: this.pageNumber,
      per_page: 10
    };
    this._CompanyService
      .getAll(data)
      .subscribe(
        (res) => {
          this.lastResponse = res;
          this.makeQueryStrings(res);
        },
        (err) => {
          console.log(err.body.msg);
        }
      )
      .add(() => {
        this.spinnerService.stopSpinner();
      });
  }

  makeQueryStrings(res) {
    this.pageNumber = res.currentPage;
    this.previousPageNumber = res.previousPage;
    this.nextPageNumber = res.nextPage;
    this.lastPageNumber = res.totalPages;
    this.totalResults = res.totalResults;
  }

}
