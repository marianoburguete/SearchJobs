import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CurriculumViewComponent } from './curriculum-view.component';

describe('CurriculumViewComponent', () => {
  let component: CurriculumViewComponent;
  let fixture: ComponentFixture<CurriculumViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CurriculumViewComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CurriculumViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
