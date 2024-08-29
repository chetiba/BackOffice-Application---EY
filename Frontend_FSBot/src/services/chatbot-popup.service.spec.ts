import { TestBed } from '@angular/core/testing';

import { ChatbotPopupService } from './chatbot-popup.service';

describe('ChatbotPopupService', () => {
  let service: ChatbotPopupService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ChatbotPopupService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
