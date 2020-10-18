import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InterviewsDetailsComponent } from './interviews-details.component';

describe('InterviewsDetailsComponent', () => {
  let component: InterviewsDetailsComponent;
  let fixture: ComponentFixture<InterviewsDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InterviewsDetailsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InterviewsDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
