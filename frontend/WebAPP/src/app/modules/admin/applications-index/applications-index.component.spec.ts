import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ApplicationsIndexComponent } from './applications-index.component';

describe('ApplicationsIndexComponent', () => {
  let component: ApplicationsIndexComponent;
  let fixture: ComponentFixture<ApplicationsIndexComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ApplicationsIndexComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ApplicationsIndexComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
