// chat-dialog.service.ts
import { Injectable } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ChatbotComponent } from '../app/chatbot/chatbot.component';

@Injectable({
  providedIn: 'root'
})
export class ChatDialogService {

  constructor(public dialog: MatDialog) {}

  openChatbot(): void {
    const dialogRef = this.dialog.open(ChatbotComponent, {
      width: '400px',
      height: '600px'
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }
}
