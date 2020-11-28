import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/http/auth.service';
import { Router } from '@angular/router';
import { UserService } from '../../services/http/user.service';
import { userSessionModel } from '../../models/userSessionModel';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  notificationsCount: number = null;
  sessionUser: userSessionModel = null;

  constructor(
    private _router: Router,
    public authService: AuthService,
    private userService: UserService
  ) { }

  ngOnInit() {
    this.getNotifications();
    setInterval(() => {this.getNotifications()}, 1000 * 60);
  }

  logout() {
    localStorage.removeItem('userSession');
    this.authService.user = null;
    this._router.navigate(['/login']);
  }

  getNotifications() {
    this.sessionUser = this.authService.getUser();
    if (this.sessionUser != null && this.sessionUser.role === 'cliente') {
      this.userService.getNotificationsCount().subscribe(res => {
        this.notificationsCount = res['results']['count'];
      });
    }
  }

}
