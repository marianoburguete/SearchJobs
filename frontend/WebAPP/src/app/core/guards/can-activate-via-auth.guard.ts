import { Route } from '@angular/compiler/src/core';
import { Injectable } from '@angular/core';
import {
  CanActivate,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
  UrlTree,
  Router, ActivatedRoute
} from '@angular/router';
import { Observable } from 'rxjs';
import { AuthService } from '../services/http/auth.service';

@Injectable({
  providedIn: 'root',
})
export class CanActivateViaAuthGuard implements CanActivate {
  constructor(
    private authService: AuthService,
    private router: Router,
    private activatedRoute: ActivatedRoute
  ) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    let url = state.url.split('/');
    if (url[1] === 'login' || url[1] === 'registro') {
      if (this.authService.isLogged()) {
        this.router.navigate(['/home']);
        return false;
      }
      return true;
    }
    else if(url[1] === 'admin'){
      if (this.authService.getRole() !== 'funcionario') {
        this.router.navigate(['/home']);
        return false;
      }
      return true;
    }
    else if(url[1] === 'usuario'){
      if (!this.authService.isLogged() || this.authService.getRole() !== 'cliente') {
        return false;
      }
      return true;
    }
  }
}
