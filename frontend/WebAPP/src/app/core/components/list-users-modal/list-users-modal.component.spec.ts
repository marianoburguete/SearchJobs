import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListUsersModalComponent } from './list-users-modal.component';

describe('ListUsersModalComponent', () => {
  let component: ListUsersModalComponent;
  let fixture: ComponentFixture<ListUsersModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ListUsersModalComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ListUsersModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
