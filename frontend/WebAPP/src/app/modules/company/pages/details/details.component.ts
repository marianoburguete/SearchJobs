import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AlertDTO } from 'src/app/core/models/alertDto';
import { CompanyService } from 'src/app/core/services/http/company.service';
import { SpinnerService } from 'src/app/core/services/spinner.service';

@Component({
  selector: 'app-details',
  templateUrl: './details.component.html',
  styleUrls: ['./details.component.scss']
})
export class DetailsComponent implements OnInit {
  alert: AlertDTO = {
    show: false,
    msg: null,
    errorCode: null,
  };

  company: any = null;
  jobs: any = null;
  mensaje: any = null;
  rating : any = null;
  id : any = null;

  constructor(
    private companyService: CompanyService,
    private spinnerService: SpinnerService,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    let pagina = null;
    this.spinnerService.callSpinner();
    this.route.queryParamMap.subscribe((params) => {
      this.id = params.get('id');
      pagina = params.get('page');
      this.companyService.details(this.id).subscribe((res) => {
        this.company = res['results'];
      }).add(() => {this.spinnerService.stopSpinner()});
    });
  }

  addRating() {
    if (this.mensaje != null && this.mensaje !== '' && this.rating != null && this.rating !== '') {
      this.spinnerService.callSpinner();
      const data  = {
        description: this.mensaje,
        score: this.rating
      };
      this.companyService.addRating(this.id, data).subscribe(res => {
        this.alert.errorCode = 'alert-primary';
        this.alert.show = true;
        this.alert.msg = 'Calificacion enviada!';
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
}
