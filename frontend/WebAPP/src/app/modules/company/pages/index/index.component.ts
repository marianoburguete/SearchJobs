import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { SpinnerService } from 'src/app/core/services/spinner.service';
import { CompanyService } from 'src/app/core/services/http/company.service';
import { companyDto } from 'src/app/core/models/companyDto';

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.scss']
})
export class IndexComponent implements OnInit {
  lastResponse: any = {};
  companiesRecomendationList: any[] = [];
  searchForm: FormGroup;
  pageNumber = 1;
  nextPageNumber = null;
  previousPageNumber = null;
  lastPageNumber = null;
  totalResults = 0;

  constructor(
    private _CompanyService: CompanyService,
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private spinnerService: SpinnerService
  ) {}

  ngOnInit() {
    this.searchForm = this.fb.group({
      search: ['', Validators.required],
    });

    this.route.queryParamMap.subscribe((params) => {
      this.searchForm.setValue({ search: params.get('search') });
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
      per_page: 10,
      search: this.searchForm.controls['search'].value
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

  searchTextRecomendations(event: Event) {
    let data: companyDto = {
      page: 1,
      per_page: 5,
      search: (event.target as HTMLInputElement).value,
    };
    if (data.search === null || data.search === '') {
      this.companiesRecomendationList = [];
    } else {
      this._CompanyService.search(data).subscribe((res) => {
        this.companiesRecomendationList = [];
        this.companiesRecomendationList = res['results'];
      });
    }
  }

  setSearchText(event: Event) {
    let txt: string = (event.target as Element).textContent;
    this.searchForm.setValue({ search: txt });
  }
}
