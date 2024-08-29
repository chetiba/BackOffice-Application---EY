import { TestBed } from '@angular/core/testing';

import { CollabuserService } from './collabuser.service';

describe('CollabuserService', () => {
  let service: CollabuserService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CollabuserService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
