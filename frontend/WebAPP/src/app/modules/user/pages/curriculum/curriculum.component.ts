import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AlertDTO } from 'src/app/core/models/alertDto';
import { cv, education, workexperience, language, category } from 'src/app/core/models/cv';
import { UserService } from 'src/app/core/services/http/user.service';
import { SpinnerService } from 'src/app/core/services/spinner.service';
import { CategoryService } from '../../../../core/services/http/category.service';
import { DatePipe } from '@angular/common';
import { count } from 'console';

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
    private router: Router,
    private datePipe: DatePipe
  ) {}

  ngOnInit() {
    this.spinnerService.callSpinner();
    this.categoryService.getAll().subscribe(res => {
      this.categoriesList = res['results'];
    });
    this.userService.getCurriculum().subscribe(res => {
      this.curriculum = res['results'];
      this.curriculum.birth_date = this.datetimeToDate(this.curriculum.birth_date);
      this.curriculum.education.forEach(x => {
        x.start_date = this.datetimeToDate(x.start_date);
        x.end_date = this.datetimeToDate(x.end_date);
      });
      this.curriculum.workexperience.forEach(x => {
        x.start_date = this.datetimeToDate(x.start_date);
        x.end_date = this.datetimeToDate(x.end_date);
      });
      this.url = 'data:image/png;base64,' + this.curriculum.avatar;
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
      this.alert.msg = 'Solo se soportan imágenes.';
      this.alert.errorCode = 'alert-danger';
      return;
    }

    let reader = new FileReader();
    reader.readAsDataURL(this.avatarFile);
    reader.onload = (_event) => {
      this.url = reader.result;
      console.log(this.url);
      console.log(this.url.substring(23));
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
        name: 'algo',
        id: null
      }
    };
    this.curriculum.categories.push(e);
  }

  removeCategories(index) {
    this.curriculum.categories.splice(index, 1);
  }

  submitCurriculum() {
    console.log(new Date((new Date().getTime() - new Date(this.curriculum.birth_date).getTime())));
    this.spinnerService.callSpinner();
    this.alert.show = false;
    if (this.curriculum.phone == null || this.curriculum.phone.length < 1) {
      this.alert.msg = 'El teléfono es obligatorio.';
      this.alert.show = true;
      this.alert.errorCode = 'alert-danger';
      this.spinnerService.stopSpinner();
    }
    else {
      this.curriculum.phone = this.curriculum.phone.toString();
    }
    if (this.curriculum.name == null || this.curriculum.name.length < 1) {
      this.alert.msg = 'El nomrbe es obligatorio.';
      this.alert.show = true;
      this.alert.errorCode = 'alert-danger';
      this.spinnerService.stopSpinner();
    }
    if (this.curriculum.birth_date == null || this.curriculum.birth_date.length < 1) {
      this.alert.msg = 'La fecha de nacimiento es obligatoria.';
      this.alert.show = true;
      this.alert.errorCode = 'alert-danger';
      this.spinnerService.stopSpinner();
    }
    else if (!this.dateGreaterThanToday(this.curriculum.birth_date)) {
      this.alert.msg = 'La fecha debe ser menor a la actual.';
      this.alert.show = true;
      this.alert.errorCode = 'alert-danger';
      this.spinnerService.stopSpinner();
    }
    else {
      let today = new Date();
      let birthdayDate = new Date(this.curriculum.birth_date);
      today.setUTCFullYear((today.getUTCFullYear() - birthdayDate.getUTCFullYear()));
      if (today.getUTCFullYear() < 18) {
        this.alert.msg = 'Debes ser mayor de dieciocho años para poder subir tu curriculum';
        this.alert.show = true;
        this.alert.errorCode = 'alert-danger';
        this.spinnerService.stopSpinner();
      }
    }
    if (this.curriculum.address == null || this.curriculum.address.length < 1) {
      this.alert.msg = 'La dirección es obligatoria.';
      this.alert.show = true;
      this.alert.errorCode = 'alert-danger';
      this.spinnerService.stopSpinner();
    }
    if (this.curriculum.country == null || this.curriculum.country.length < 1) {
      this.alert.show = true;
      this.alert.errorCode = 'alert-danger';
      this.alert.msg = 'El país es obligatorio.';
      this.spinnerService.stopSpinner();
    }

    this.curriculum.education.forEach(x => {
      if (x.start_date == null) {
        this.alert.show = true;
        this.alert.errorCode = 'alert-danger';
        this.alert.msg = 'Las fechas de inicio no pueden estar vacías';
        this.spinnerService.stopSpinner();
      }
      else if (!this.dateGreaterThanToday(x.start_date)){
        this.alert.msg = 'La fecha debe ser menor a la actual.';
        this.alert.show = true;
        this.alert.errorCode = 'alert-danger';
        this.spinnerService.stopSpinner();
      }
      else if (x.end_date !== null){
        if (new Date(x.start_date).getTime() > new Date(x.end_date).getTime()) {
          this.alert.show = true;
          this.alert.errorCode = 'alert-danger';
          this.alert.msg = 'Las fechas de finalización no pueden ser menores a las de inicio';
          this.spinnerService.stopSpinner();
        }
      }
    });
    
    this.curriculum.workexperience.forEach(x => {
      if (x.start_date == null) {
        this.alert.show = true;
        this.alert.errorCode = 'alert-danger';
        this.alert.msg = 'Las fechas de inicio no pueden estar vacía';
        this.spinnerService.stopSpinner();
      }
      else if (x.end_date !== null){
        if (new Date(x.start_date).getTime() > new Date(x.end_date).getTime()) {
          this.alert.show = true;
          this.alert.errorCode = 'alert-danger';
          this.alert.msg = 'Las fechas de finalización no pueden ser menores a las de inicio';
          this.spinnerService.stopSpinner();
        }
      }
    });

    if (this.curriculum.categories.length < 1) {
      this.alert.show = true;
      this.alert.errorCode = 'alert-danger';
      this.alert.msg = 'Debes seleccionar al menos una categoría de interés';
      this.spinnerService.stopSpinner();
    }
    else {
      this.curriculum.categories.sort(x => x.category.id);
      for (let i = 0; i < this.curriculum.categories.length-1; i++) {
        const element = this.curriculum.categories[i];
          if (element.category.id == this.curriculum.categories[i+1].category.id) {
            this.alert.show = true;
            this.alert.errorCode = 'alert-danger';
            this.alert.msg = 'No se deben repetir categorías de interés';
            this.spinnerService.stopSpinner();
          }
      }
    }

    if (this.alert.show === false) {
      if (this.curriculum.id == null) {
        if (this.url !== null) {
          this.curriculum.avatar = this.url.substring(this.url.indexOf(',')+1);
        }
        // Convertimos las fechas de tipo DATE a DATETIME porque la API las pide
        this.curriculum.birth_date = this.dateToDatetime(this.curriculum.birth_date).toISOString().slice(0, -1);
        this.curriculum.education.forEach(x => {
          if (x.start_date !== null) {
            let t = this.dateToDatetime(x.start_date);
            x.start_date = t.toISOString().slice(0, -1);
          }
          if (x.end_date !== null) {
            let t = this.dateToDatetime(x.end_date);
            x.end_date = t.toISOString().slice(0, -1);
          }
        });
        this.curriculum.workexperience.forEach(x => {
          if (x.start_date !== null) {
            let t = this.dateToDatetime(x.start_date);
            x.start_date = t.toISOString().slice(0, -1);
          }
          if (x.end_date !== null) {
            let t = this.dateToDatetime(x.end_date);
            x.end_date = t.toISOString().slice(0, -1);
          }
        });
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
        if (this.url !== null) {
          this.curriculum.avatar = this.url.substring(this.url.indexOf(',')+1);
        }
        this.curriculum.birth_date = this.dateToDatetime(this.curriculum.birth_date).toISOString().slice(0, -1);
        this.curriculum.education.forEach(x => {
          if (x.start_date !== null) {
            let t = this.dateToDatetime(x.start_date);
            x.start_date = t.toISOString().slice(0, -1);
          }
          if (x.end_date !== null) {
            let t = this.dateToDatetime(x.end_date);
            x.end_date = t.toISOString().slice(0, -1);
          }
        });
        this.curriculum.workexperience.forEach(x => {
          if (x.start_date !== null) {
            let t = this.dateToDatetime(x.start_date);
            x.start_date = t.toISOString().slice(0, -1);
          }
          if (x.end_date !== null) {
            let t = this.dateToDatetime(x.end_date);
            x.end_date = t.toISOString().slice(0, -1);
          }
        });
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

  dateToDatetime(x) {
    let a = new Date(x);
    console.log(a.toISOString());
    return a;
  }
  
  datetimeToDate(x) {
    let a = this.datePipe.transform(x, 'yyyy-MM-dd');
    return a;
  }

  dateGreaterThanToday(x) {
    let a = new Date(x);
    if (a.getTime() > new Date().getTime()) {
      return false;
    }
    return true;
  }

}
