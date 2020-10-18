import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListJobsModalComponent } from './list-jobs-modal.component';

describe('ListJobsModalComponent', () => {
  let component: ListJobsModalComponent;
  let fixture: ComponentFixture<ListJobsModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ListJobsModalComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ListJobsModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
