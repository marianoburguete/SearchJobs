import { Component, OnInit } from '@angular/core';
import { AlertDTO } from 'src/app/core/models/alertDto';
import { JobService } from '../../../core/services/http/job.service';
import { SpinnerService } from '../../../core/services/spinner.service';
import { CategoryService } from '../../../core/services/http/category.service';
import { UserService } from '../../../core/services/http/user.service';
import { language, category } from '../../../core/models/cv';

@Component({
  selector: 'app-user-recommendations',
  templateUrl: './user-recommendations.component.html',
  styleUrls: ['./user-recommendations.component.scss']
})
export class UserRecommendationsComponent implements OnInit {

  alert: AlertDTO = {
    show: false,
    msg: null,
    errorCode: null,
  };

  categoriesList: any = [];
  categoryFilter: any = null;
  languageFilter: string = null;
  minAgeFilter: string = null;
  maxAgeFilter: string = null;

  usersList: any = [];

  constructor(
    private userService: UserService,
    private categoryService: CategoryService,
    private spinnerService: SpinnerService
  ) { }

  ngOnInit() {
    this.spinnerService.callSpinner();
    this.categoryService.getAll().subscribe(res =>{
      this.categoriesList = res['results'];
    }).add(() => this.spinnerService.stopSpinner());
  }

  searchUsers() {
    this.spinnerService.callSpinner();
    const data = {
      filters: {
        language: this.languageFilter,
        category: parseInt(this.categoryFilter, 10),
        ageRange: {
          minAge: this.minAgeFilter != null ? parseInt(this.minAgeFilter, 10) : null,
          maxAge: this.maxAgeFilter != null ? parseInt(this.maxAgeFilter, 10) : null,
        }
      }
    }
    this.userService.recommendedUsers(data).subscribe(res => {
      this.usersList = res['results'];
    }).add(() => this.spinnerService.stopSpinner());
  }
}
