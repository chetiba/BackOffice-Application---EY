import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PositionnementComponent } from './positionnement.component';

describe('PositionnementComponent', () => {
  let component: PositionnementComponent;
  let fixture: ComponentFixture<PositionnementComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PositionnementComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PositionnementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
