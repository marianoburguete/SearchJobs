import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AlertDTO } from 'src/app/core/models/alertDto';
import { SpinnerService } from 'src/app/core/services/spinner.service';

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.scss']
})
export class IndexComponent implements OnInit {

  alert: AlertDTO = {
    show: false,
    msg: null,
    errorCode: null
  }

  constructor(private spinnerService: SpinnerService, private route: ActivatedRoute, private router: Router) { }

  ngOnInit(): void {
  }

}
