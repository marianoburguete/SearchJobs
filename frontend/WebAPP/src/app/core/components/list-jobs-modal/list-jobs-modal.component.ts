import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { SpinnerService } from '../../services/spinner.service';
import { JobService } from '../../services/http/job.service';

@Component({
  selector: 'app-list-jobs-modal',
  templateUrl: './list-jobs-modal.component.html',
  styleUrls: ['./list-jobs-modal.component.scss']
})
export class ListJobsModalComponent implements OnInit {

  public searchText: string;
  results: any = null;

  @Output() jobIdEvent = new EventEmitter<any>();

  constructor(private jobService: JobService, private spinnerService: SpinnerService) { }

  ngOnInit(): void {
  }

  searchJob() {
    this.spinnerService.callSpinner();
    const data = {
      title: this.searchText
    }
    this.jobService.searchJobByTitle(data).subscribe((res) => {
      if (res['jobs'] !== {}) {
        this.results = res['jobs'];
      }
      else {
        this.results = null;
      }
    }).add(() => this.spinnerService.stopSpinner());
  }

  setSearchText(event:Event) {
    this.searchText = (event.target as HTMLInputElement).value;
    console.log(this.searchText);
  }

  setJobId(ind) {
    let r = this.results[ind];
    this.jobIdEvent.emit(r);
  }

}
