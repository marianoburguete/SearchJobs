import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AlertDTO } from 'src/app/core/models/alertDto';
import { AuthService } from 'src/app/core/services/http/auth.service';
import { SpinnerService } from 'src/app/core/services/spinner.service';
import { UserService } from '../../../../core/services/http/user.service';

@Component({
  selector: 'app-notifications',
  templateUrl: './notifications.component.html',
  styleUrls: ['./notifications.component.scss']
})
export class NotificationsComponent implements OnInit {

  alert: AlertDTO = {
    show: false,
    msg: null,
    errorCode: null,
  };

  pageFilter = 1;
  totalPagesFilter: number = null;

  notificationsList: any[] = [];

  constructor(
    private userService: UserService,
    private spinnerService: SpinnerService,
    private route: ActivatedRoute,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.getAll();
  }

  getAll() {
    this.spinnerService.callSpinner();
    const data = {
      page: this.pageFilter
    };
    this.userService.getNotifications(data).subscribe(res => {
      res['results'].forEach(n => {
        this.notificationsList.push(n);
        if (n.status === 'unread') {
          this.userService.updateNotificationStatus(n.id).subscribe(res => {});
        }
      });
      this.pageFilter++;
      this.totalPagesFilter = res['totalPages'];
    },err => {
      this.alert.show = true;
      this.alert.msg = err.msg;
      this.alert.errorCode = 'alert-danger';
    }).add(() => this.spinnerService.stopSpinner());
  }

}
