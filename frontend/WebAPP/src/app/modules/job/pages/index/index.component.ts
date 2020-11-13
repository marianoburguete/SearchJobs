import { Component, OnInit } from '@angular/core';
import { JobService } from '../../../../core/services/http/job.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { searchJobDto } from '../../../../core/models/searchJobDto';
import { element } from 'protractor';
import { ActivatedRoute } from '@angular/router';
import { SpinnerService } from '../../../../core/services/spinner.service';
import { CategoryService } from '../../../../core/services/http/category.service';
import { category } from '../../../../core/models/cv';

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.scss'],
})
export class IndexComponent implements OnInit {
  lastResponse: any = {};
  jobsRecomendationList: any[] = [];
  searchForm: FormGroup;
  filterQuery: string = null;
  workdayFilter = '';
  salaryFilter: string;
  locationFilter: string = null;
  remoteFilter: boolean = null;
  categoryFilter: string = null;
  categoriesList: any = [];
  pageNumber = 1;
  nextPageNumber = null;
  previousPageNumber = null;
  lastPageNumber = null;
  totalResults = 0;

  tempSearch = null;

  constructor(
    private _jobService: JobService,
    private categoryService: CategoryService,
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private spinnerService: SpinnerService
  ) {}

  ngOnInit() {
    this.searchForm = this.fb.group({
      search: ['', Validators.required],
    });
    this.categoryService.getAll().subscribe(res => {
      this.categoriesList = res['results'];
      this.categoriesList.sort((a, b) => (a.name > b.name) ? 1 : -1);
    });
    this.route.queryParamMap.subscribe((params) => {
      this.searchForm.setValue({ search: params.get('search') });
      if (params.get('jornada') != null) {
        this.workdayFilter = params.get('jornada');
      } else {
        this.workdayFilter = 'Cualquiera';
      }
      if (params.get('categoria') != null) {
        this.categoryFilter = params.get('categoria');
      } else {
        this.categoryFilter = 'Cualquiera';
      }
      if (params.get('salarioMin') != null) {
        this.salaryFilter = params.get('salarioMin');
      } else {
        this.salaryFilter = null;
      }
      if (params.get('remote') != null) {
        if (params.get('remote') === 'true') {
          this.remoteFilter = true;
        } else {
          if (params.get('location') != null) {
            this.locationFilter = params.get('location');
          }
        }
      } else {
        this.remoteFilter = false;
      }
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
    let data: searchJobDto;
    data = {
      page: this.pageNumber,
      per_page: 10,
      search: this.searchForm.controls['search'].value,
      workday: this.workdayFilter != 'Cualquiera' ? this.workdayFilter : null,
      category: this.categoryFilter != 'Cualquiera' ? parseInt(this.categoryFilter) : null,
      minSalary: this.salaryFilter,
      location:
        this.remoteFilter === false
          ? this.locationFilter != null
            ? this.locationFilter
            : null
          : 'remote',
    };
    this._jobService
      .search(data)
      .subscribe(
        (res) => {
          this.lastResponse = res;
          this.jobsRecomendationList = [];
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
    this.tempSearch = (event.target as HTMLInputElement).value;
    let data: searchJobDto = {
      page: 1,
      per_page: 5,
      search: (event.target as HTMLInputElement).value,
    };
    if (data.search === null || data.search === '') {
      this.jobsRecomendationList = [];
    } else {
      this._jobService.search(data).subscribe((res) => {
        this.jobsRecomendationList = [];
        this.jobsRecomendationList = res['results'];
      });
    }
  }

  setSearchText(event: Event) {
    let txt: string = (event.target as Element).textContent;
    this.searchForm.setValue({ search: txt });
  }

  createdAt(d) {
    let da: any = new Date(d);
    let now: any = new Date();
    return Math.floor((now - da) / (1000 * 60 * 60 * 24));
  }
}
