import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
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
  newMessage: any = null;

  constructor(
    private companyService: CompanyService,
    private spinnerService: SpinnerService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit() {
    this.spinnerService.callSpinner();
    this.route.paramMap.subscribe((params) => {
      this.companyService
        .get({ id: params.get('id') })
        .subscribe((res) => {
          this.company = res['results'];
        })
        .add(() => this.spinnerService.stopSpinner());
    });
  }

  addMessage() {
    if (this.newMessage != null && this.newMessage !== '') {
      this.spinnerService.callSpinner();
      const data  = {
        id: this.company.id,
        text: this.newMessage
      };
      this.companyService.addMessage(data).subscribe(res => {
        this.alert.errorCode = 'alert-primary';
        this.alert.show = true;
        this.alert.msg = 'Mensaje enviado';
        this.company.commentaries = res['results'];
        this.newMessage = null;
      }, err => {
        this.alert.errorCode = 'alert-danger';
          this.alert.show = true;
          this.alert.msg = err.error.msg;
      }).add(() => this.spinnerService.stopSpinner());
    }
  }

}
