import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/http/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  constructor(
    private _router: Router,
    public authService: AuthService
  ) { }

  ngOnInit(): void {
  }

  logout() {
    localStorage.removeItem('userSession');
    this.authService.user = null;
    this._router.navigate(['/login']);
  }

}
