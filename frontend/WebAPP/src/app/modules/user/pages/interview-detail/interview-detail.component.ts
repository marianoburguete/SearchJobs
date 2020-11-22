import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AlertDTO } from 'src/app/core/models/alertDto';
import { SpinnerService } from 'src/app/core/services/spinner.service';
import { InterviewService } from '../../../../core/services/http/interview.service';
import { AuthService } from '../../../../core/services/http/auth.service';

@Component({
  selector: 'app-interview-detail',
  templateUrl: './interview-detail.component.html',
  styleUrls: ['./interview-detail.component.scss'],
})
export class InterviewDetailComponent implements OnInit {
  alert: AlertDTO = {
    show: false,
    msg: null,
    errorCode: null,
  };

  userSession: any = null;

  interview: any = null;
  newMessage: string = null;

  interviewId: any;

  constructor(
    private authService: AuthService,
    private interviewService: InterviewService,
    private spinnerService: SpinnerService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit() {
    this.route.paramMap.subscribe((params) => {
      this.userSession = this.authService.getUser();
      this.spinnerService.callSpinner();
      const data = {
        id: params.get('id'),
      };
      this.interviewId = params.get('id');
      this.interviewService
        .getInterviewForUser(data)
        .subscribe(
          (res) => {
            this.interview = res['results'];
          },
          (err) => {
            this.alert.errorCode = 'alert-danger';
            this.alert.show = true;
            this.alert.msg = err.error.msg;
          }
        )
        .add(() => this.spinnerService.stopSpinner());
    });
    setInterval(() => {this.getNewMessages()}, 1000 * 10);
  }

  messageWho(id):string {
    if (id === this.userSession.id) {
      return this.userSession.email;
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
      .getInterviewForUser(data)
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
}
