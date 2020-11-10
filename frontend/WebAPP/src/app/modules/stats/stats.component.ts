import { Component, OnInit } from '@angular/core';
import { AlertDTO } from 'src/app/core/models/alertDto';
import { SpinnerService } from 'src/app/core/services/spinner.service';
import { StatsService } from '../../core/services/http/stats.service';

@Component({
  selector: 'app-stats',
  templateUrl: './stats.component.html',
  styleUrls: ['./stats.component.scss']
})
export class StatsComponent implements OnInit {
  alert: AlertDTO = {
    show: false,
    msg: null,
    errorCode: null
  }

  results: any = null;
  applicationsXInterviews: any = null;
  popularSearches: any = null;

  viewPerCategory: any[] = [700, 800];

  colorSchemeAxI = {
    domain: [ '#E44D25', '#CFC0BB']
  };
  view: any[] = [700, 300];

  // options
  legendAxI: boolean = true;
  showLabelsAxI: boolean = true;
  animationsAxI: boolean = true;
  xAxisAxI: boolean = true;
  yAxisAxI: boolean = true;
  showYAxisLabelAxI: boolean = true;
  showXAxisLabelAxI: boolean = true;
  xAxisLabelAxI: string = 'Fecha';
  yAxisLabelAxI: string = 'Cantidad';
  timelineAxI: boolean = true;



  constructor(
    private statsService: StatsService,
    private spinnerService: SpinnerService
  ) {
    if (innerWidth < 929) {
      this.viewPerCategory = [innerWidth / 1.3, 1200];
    } else {
      this.viewPerCategory = [innerWidth / 1.3, 400];
    }
  }

  ngOnInit() {
    this.spinnerService.callSpinner();
    this.statsService.getStats().subscribe(res => {
      this.results = res['results'];

      this.applicationsXInterviews = [];
      let a = {
        name: 'Postulaciones',
        series: []
      };
      let i = {
        name: 'Entrevistas',
        series: []
      };
      this.results['applicationsXInterviews'].forEach(x => {
        a.series.push({
          value: x.applications,
          name: x.day
        });
        i.series.push({
          value: x.interviews,
          name: x.day
        });
      });
      this.applicationsXInterviews.push(a);
      this.applicationsXInterviews.push(i);

      this.popularSearches = [];
      this.results['popularSearches'].forEach(x => {
        this.popularSearches.push(
          {
            name: x.text,
            value: x.count
          }
        );
      });
    },
    err => {
      this.alert.show = true;
      this.alert.msg = err.error.msg;
      this.alert.errorCode = 'alert-danger';
    }).add(() => this.spinnerService.stopSpinner());
  }

  onResizePerCategory(event) {
    if (innerWidth < 929) {
      this.viewPerCategory = [innerWidth / 1.3, 1200];
    } else {
      this.viewPerCategory = [innerWidth / 1.3, 400];
    }
  }

}
