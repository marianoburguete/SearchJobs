import { Target } from '@angular/compiler';
import { Input, Output, EventEmitter } from '@angular/core';
import { Component, OnInit } from '@angular/core';
import { UserService } from '../../services/http/user.service';
import { SpinnerService } from '../../services/spinner.service';

@Component({
  selector: 'app-list-users-modal',
  templateUrl: './list-users-modal.component.html',
  styleUrls: ['./list-users-modal.component.scss']
})
export class ListUsersModalComponent implements OnInit {

  public searchText: string;
  results: any = null;

  @Output() userIdEvent = new EventEmitter<any>();

  constructor(private userService: UserService, private spinnerService: SpinnerService) { }

  ngOnInit(): void {
  }

  searchUser() {
    this.spinnerService.callSpinner();
    const data = {
      email: this.searchText
    }
    this.userService.searchUsersByEmail(data).subscribe((res) => {
      if (res['user'] !== {}) {
        this.results = res['users'];
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

  setUserId(ind) {
    this.userIdEvent.emit(this.results[ind]);
  }

}
