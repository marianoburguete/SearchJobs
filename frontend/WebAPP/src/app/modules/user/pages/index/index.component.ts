import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AlertDTO } from 'src/app/core/models/alertDto';
import { cv } from 'src/app/core/models/cv';
import { UserService } from 'src/app/core/services/http/user.service';
import { SpinnerService } from 'src/app/core/services/spinner.service';

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.scss'],
})
export class IndexComponent implements OnInit {
  alert: AlertDTO = {
    show: false,
    msg: null,
    errorCode: null,
  };

  curriculum: cv = {
    education: [],
    workexperience: [],
    languages: [],
    categories: [],
  };

  salaryEstimate: any = null;

  multi: any[] = [];
  view: any[] = [700, 400];
  viewPerCategory: any[] = [400, 250];

  // options
  showXAxis: boolean = true;
  showYAxis: boolean = true;
  gradient: boolean = false;
  showXAxisLabel: boolean = true;
  xAxisLabel: string = 'Categorías';
  showYAxisLabel: boolean = true;
  yAxisLabel: string = 'Salario';
  showLegend: boolean = false;
  legendTitle: string = 'Years';

  colorScheme = {
    domain: ['#5AA454', '#C7B42C', '#AAAAAA'],
  };

  constructor(
    private userService: UserService,
    private spinnerService: SpinnerService,
    private route: ActivatedRoute,
    private router: Router
  ) {
    if (innerWidth < 929) {
      this.viewPerCategory = [innerWidth / 1.3, 1200];
    } else {
      this.viewPerCategory = [innerWidth / 1.3, 400];
    }
  }

  ngOnInit() {
    this.spinnerService.callSpinner();
    this.userService
      .getCurriculum()
      .subscribe(
        (res) => {
          this.curriculum = res['results'];
          if (this.curriculum !== null) {
            this.userService.estimateSalary().subscribe(
              (res) => {
                this.salaryEstimate = res['results'];
                let pruebaAverquepasa = [];
                res['results'].forEach((x) => {
                  pruebaAverquepasa.push({
                    name: x.name,
                    series: [
                      {
                        name: 'Mínimo',
                        value: x.minimum,
                      },
                      {
                        name: 'Promedio',
                        value: x.estimation,
                      },
                      {
                        name: 'Máximo',
                        value: x.maximum,
                      },
                    ],
                  });
                });
                this.multi  = pruebaAverquepasa;
              },
              (err) => {
                this.alert.show = true;
                this.alert.msg = err.error.msg;
                this.alert.errorCode = 'alert-danger';
              }
            );
          }
        },
        (err) => {
          if (err.status === 404) {
            this.router.navigate(['/usuario/cv/editar']);
          } else {
            this.alert.show = true;
            this.alert.msg = err.error.msg;
            this.alert.errorCode = 'alert-danger';
          }
        }
      )
      .add(() => this.spinnerService.stopSpinner());
  }

  onResizePerCategory(event) {
    if (innerWidth < 929) {
      this.viewPerCategory = [innerWidth / 1.3, 900];
    } else {
      this.viewPerCategory = [innerWidth / 1.3, 400];
    }
  }
}
