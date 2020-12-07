import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AlertDTO } from 'src/app/core/models/alertDto';
import { InterviewService } from 'src/app/core/services/http/interview.service';
import { SpinnerService } from 'src/app/core/services/spinner.service';

@Component({
  selector: 'app-interviews-details',
  templateUrl: './interviews-details.component.html',
  styleUrls: ['./interviews-details.component.scss'],
})
export class InterviewsDetailsComponent implements OnInit {
  alert: AlertDTO = {
    show: false,
    msg: null,
    errorCode: null,
  };

  interview: any = null;

  newMessage: any = null;

  prueba: any = null;

  interviewId: any;

  changeDate = false;

  constructor(
    private interviewService: InterviewService,
    private spinnerService: SpinnerService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit() {
    console.log('Change date status: ', this.changeDate);
    this.spinnerService.callSpinner();
    this.route.paramMap.subscribe((params) => {
      this.interviewId = params.get('id');
      this.interviewService
        .get({ id: params.get('id') })
        .subscribe((res) => {
          this.interview = res['results'];
        })
        .add(() => this.spinnerService.stopSpinner());
    });
    setInterval(() => {this.getNewMessages()}, 1000 * 10);
  }

  pruebaPrint() {
    this.spinnerService.callSpinner();
    let data = {
      id: this.interview.id,
      date_interview: this.interview.date_interview,
      results: this.interview.results,
      status: this.interview.status,
    };
    this.interviewService
      .put(data)
      .subscribe(
        (res) => {
          this.interview = res['results'];
          this.alert.errorCode = 'alert-primary';
          this.alert.show = true;
          this.alert.msg = res['msg'];
        },
        (err) => {
          this.alert.errorCode = 'alert-danger';
          this.alert.show = true;
          this.alert.msg = err.error.msg;
        }
      )
      .add(() => this.spinnerService.stopSpinner());
  }

  messageWho(id):string {
    if (id === this.interview.user.id) {
      return this.interview.user.email;
    } else {
      return 'Administrador';
    }
  }

  addMessage() {
    if (this.newMessage != null && this.newMessage !== '') {
      this.spinnerService.callSpinner();
      const data  = {
        id: this.interview.id,
        text: this.newMessage
      };
      this.interviewService.addMessage(data).subscribe(res => {
        this.alert.errorCode = 'alert-primary';
        this.alert.show = true;
        this.alert.msg = 'Mensaje enviado';
        this.interview.messages = res['results'];
        this.newMessage = null;
      }, err => {
        this.alert.errorCode = 'alert-danger';
          this.alert.show = true;
          this.alert.msg = err.error.msg;
      }).add(() => this.spinnerService.stopSpinner());
    }
  }

  getNewMessages() {
    const data = {
      id: this.interviewId,
    };
    this.interviewService
      .get(data)
      .subscribe(
        (res) => {
          this.interview.messages = res['results']['messages']
        },
        (err) => {
          this.alert.errorCode = 'alert-danger';
          this.alert.show = true;
          this.alert.msg = err.error.msg;
        }
    );
  }

  changeDateF() {
    this.changeDate = true;
  }
}
