import { Component, OnInit } from '@angular/core';
import { AlertDTO } from 'src/app/core/models/alertDto';
import { SpinnerService } from 'src/app/core/services/spinner.service';
import { StatsService } from '../../core/services/http/stats.service';
import { CategoriesNamesPipe } from '../../core/pipes/categories-pipe';

@Component({
  selector: 'app-stats',
  templateUrl: './stats.component.html',
  styleUrls: ['./stats.component.scss'],
  providers: [CategoriesNamesPipe]
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

  colorSchemeCategories = {
    domain:  ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6', 
    '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
    '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A', 
    '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
    '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC', 
    '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
    '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680', 
    '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
    '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3', 
    '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF']
  };

  colorSchemeAxI = {
    domain: [ '#E44D25', '#00B3E6']
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
    private spinnerService: SpinnerService,
    private categoriesNamePipe: CategoriesNamesPipe
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

      this.results['jobsPerCategoryCount'].forEach(x => {
        x.name = this.categoriesNamePipe.transform(x['name']);
      });

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
