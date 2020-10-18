import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InterviewsIndexComponent } from './interviews-index.component';

describe('InterviewsIndexComponent', () => {
  let component: InterviewsIndexComponent;
  let fixture: ComponentFixture<InterviewsIndexComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InterviewsIndexComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InterviewsIndexComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
