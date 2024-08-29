import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChatbotPopupService {
  private display = new BehaviorSubject<boolean>(false);
  public display$ = this.display.asObservable();

  constructor() { }

  toggleDisplay(): void {
    this.display.next(!this.display.value);
  }
}
