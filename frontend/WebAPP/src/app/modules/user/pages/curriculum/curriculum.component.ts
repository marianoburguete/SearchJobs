import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AlertDTO } from 'src/app/core/models/alertDto';
import { cv, education, workexperience, language, category } from 'src/app/core/models/cv';
import { UserService } from 'src/app/core/services/http/user.service';
import { SpinnerService } from 'src/app/core/services/spinner.service';
import { CategoryService } from '../../../../core/services/http/category.service';

@Component({
  selector: 'app-curriculum',
  templateUrl: './curriculum.component.html',
  styleUrls: ['./curriculum.component.scss']
})
export class CurriculumComponent implements OnInit {

  alert: AlertDTO = {
    show: false,
    msg: null,
    errorCode: null,
  };

  curriculumExists = true;
  categoriesList:any = null;

  curriculum: cv = {
    education: [],
    workexperience: [],
    languages: [],
    categories: []
  };
  avatarFile: File;
  url = null;

  constructor(
    private userService: UserService,
    private categoryService: CategoryService,
    private spinnerService: SpinnerService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit() {
    this.spinnerService.callSpinner();
    this.categoryService.getAll().subscribe(res => {
      this.categoriesList = res['results'];
    });
    this.userService.getCurriculum().subscribe(res => {
      this.curriculum = res['results'];
    },
    err => {
      if (err.error.msg === 'No existe ningun curriculum asociado al usuario indicado.') {
        this.curriculumExists = false;
      }
      else{
        this.alert.show = true;
        this.alert.msg = err.error.msg;
        this.alert.errorCode = 'alert-danger';
      }
    }).add(() => this.spinnerService.stopSpinner());
  }

  onFileChanged(event) {
    this.avatarFile = event.target.files[0];
    var mimeType = this.avatarFile.type;

    if (mimeType.match(/image\/*/) == null) {
      this.alert.show = true;
      this.alert.msg = 'Only images are supported';
      this.alert.errorCode = 'alert-danger';
      return;
    }

    let reader = new FileReader();
    reader.readAsDataURL(this.avatarFile);
    reader.onload = (_event) => {
      this.url = reader.result;
    };
  }

  addEducation() {
    const e: education = {
      name: null,
      place: null,
      start_date: null,
      end_date: null
    };
    this.curriculum.education.push(e);
  }

  removeEducation(index) {
    this.curriculum.education.splice(index, 1);
  }
  
  addWorkexperience() {
    const e: workexperience = {
      name: null,
      ocupation: null,
      start_date: null,
      end_date: null
    };
    this.curriculum.workexperience.push(e);
  }

  removeWorkexperience(index) {
    this.curriculum.workexperience.splice(index, 1);
  }
  
  addLanguages() {
    const e: language = {
      name: null
    };
    this.curriculum.languages.push(e);
  }

  removeLanguages(index) {
    this.curriculum.languages.splice(index, 1);
  }
  
  addCategories() {
    const e: category = {
      category: {
        name: null,
        id: null
      }
    };
    this.curriculum.categories.push(e);
  }

  removeCategories(index) {
    this.curriculum.categories.splice(index, 1);
  }

  submitCurriculum() {
    this.spinnerService.callSpinner();
    this.alert.show = false;
    if (this.curriculum.phone == null) {
      this.alert.msg = 'El teléfono es obligatorio.';
      this.alert.show = true;
      this.alert.errorCode = 'alert-danger';
    }
    else {
      this.curriculum.phone = this.curriculum.phone.toString();
    }
    if (this.curriculum.name == null) {
      this.alert.msg = 'El nomrbe es obligatorio.';
      this.alert.show = true;
      this.alert.errorCode = 'alert-danger';
    }
    if (this.curriculum.birth_date == null) {
      this.alert.msg = 'la fecha de nacimiento es obligatoria.';
      this.alert.show = true;
      this.alert.errorCode = 'alert-danger';
    }
    if (this.curriculum.address == null) {
      this.alert.msg = 'La dirección es obligatoria.';
      this.alert.show = true;
      this.alert.errorCode = 'alert-danger';
    }
    if (this.curriculum.country == null) {
      this.alert.show = true;
      this.alert.errorCode = 'alert-danger';
      this.alert.msg = 'El país es obligatorio.';
    }

    if (this.alert.show === false) {
      if (this.curriculum.id == null) {
        this.userService.addCurriculum(this.curriculum).subscribe(res => {
          this.router.navigate(['usuario/cv']);
        },
        err => {
          this.alert.show = true;
          this.alert.msg = err.error.msg;
          this.alert.errorCode = 'alert-danger';
        }).add(() => this.spinnerService.stopSpinner());
      }
      else{
        this.userService.updateCurriculum(this.curriculum).subscribe(res => {
          this.router.navigate(['usuario/cv']);
        },
        err => {
          this.alert.show = true;
          this.alert.msg = err.error.msg;
          this.alert.errorCode = 'alert-danger';
        }).add(() => this.spinnerService.stopSpinner());
      }
    }
    else {
      this.spinnerService.stopSpinner();
    }
  }

}
