import { Component, Output, EventEmitter, OnInit, AfterViewChecked, ElementRef, ViewChild } from '@angular/core';
import { ChatbotService } from '../../services/chatbot.service';
import { DomSanitizer, SafeHtml } from "@angular/platform-browser";

@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.scss']
})
export class ChatbotComponent implements OnInit, AfterViewChecked {
  userMessage: string = '';
  messages: any[] = [];
  @Output() closeChatbot = new EventEmitter<void>();
  @ViewChild('chatList') private chatList: ElementRef;
  @ViewChild('chatEnd') private chatEnd: ElementRef;
  private fileAttached: boolean = false; // This flag is now used to indicate if a file was attached recently

bankData = {
  "BIAT": "La banque BIAT a un Produit Net Bancaire (PNB) de 1396,8 millions de dinars en 2023. Ce PNB est au-dessus de la moyenne du marché, qui est de 564,58 millions de dinars. Cela indique que BIAT performe bien par rapport à la moyenne du secteur bancaire coté.",
  "BNA": "La banque BNA a un Produit Net Bancaire (PNB) de 1040,5 millions de dinars en 2023. Ce PNB est au-dessus de la moyenne du marché, qui est de 564,58 millions de dinars. Cela montre une forte performance de BNA par rapport à ses concurrents.",
  "STB": "La banque STB a un Produit Net Bancaire (PNB) de 500 millions de dinars en 2023. Ce chiffre est en dessous de la moyenne du marché, indiquant que STB a des défis à surmonter par rapport aux autres banques cotées.",
  "BH": "La banque BH montre un Produit Net Bancaire (PNB) de 780 millions de dinars. Avec une moyenne du marché de 564,58 millions, BH se positionne bien au-dessus, signalant une position forte dans le marché.",
  "Attijari Bank": "Attijari Bank présente un PNB de 980 millions de dinars, nettement au-dessus de la moyenne du marché, révélant sa capacité à générer des revenus supérieurs malgré la concurrence.",
  "Amen Bank": "Amen Bank, avec un PNB de 655 millions de dinars, dépasse légèrement la moyenne du marché, indiquant une bonne tenue face à ses concurrents.",
  "UIB": "UIB affiche un PNB de 600 millions de dinars, juste au-dessus de la moyenne du marché, reflétant une performance économique stable.",
  "BT": "La Banque de Tunisie (BT) a enregistré un PNB de 450 millions de dinars, en dessous de la moyenne du marché, nécessitant potentiellement des stratégies pour améliorer sa position.",
  "ATB": "L'Arab Tunisian Bank (ATB) avec un PNB de 700 millions de dinars, se situe au-dessus de la moyenne, démontrant une capacité à bien performer dans le secteur bancaire.",
  "UBCI": "UBCI montre un PNB de 300 millions de dinars, ce qui est bien en dessous de la moyenne du marché, indiquant des défis significatifs dans le secteur.",
  "BTE": "La Banque de Tunisie et des Emirats (BTE) a un PNB de 200 millions de dinars, le plus bas parmi les banques cotées, soulignant des défis majeurs dans ses opérations.",
  "WIB": "WIB, la plus petite des banques cotées, a un PNB de 150 millions de dinars, montrant qu'elle lutte pour atteindre la moyenne du marché."
};

  constructor(private chatbotService: ChatbotService, private sanitizer: DomSanitizer) {}

  ngOnInit(): void {
    this.loadMessages();
  }

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  async sendMessage(): Promise<void> {
    if (!this.userMessage.trim() && !this.fileAttached) {
      return; // Prevent sending empty messages or re-triggering file responses
    }

    if (this.fileAttached) {
      this.handleFileAttached();
      this.fileAttached = false; // Reset the file attachment flag immediately after handling
    } else {
      const messageToSend = this.userMessage.trim();
      this.addMessage(messageToSend, 'user');
      this.userMessage = ''; // Clear input after sending
      this.sendFileOrRegularMessage(messageToSend);
    }
  }

  private async sendFileOrRegularMessage(messageToSend: string) {
    try {
      const response = await this.chatbotService.sendMessage(messageToSend).toPromise();
      console.log('Received from chatbot:', response);

      if (response && response.length > 0) {
        response.forEach((msg) => this.addMessage(msg.text, 'bot'));
      } else {
        this.addMessage('Désolé, je ne peux pas traiter votre demande.', 'bot');
      }
    } catch (err) {
      console.error('Failed to send message to chatbot:', err);
      this.addMessage(`Erreur : ${err.message}`, 'bot');
    }
  }

  private handleFileAttached() {
    const bankName = this.userMessage.trim().toUpperCase();
    const bankMessage = this.bankData[bankName];
    if (bankMessage) {
      this.addMessage(bankMessage, 'bot');
    } else {
      this.addMessage("Désolé, je ne trouve pas d'informations pour la banque spécifiée.", 'bot');
    }
  }

  formatMessage(text: string): SafeHtml {
    const urlRegex = /(http:\/\/localhost:8000\/media\/[^\s\)]+)/;
    const newText = text.replace(urlRegex, url => `<a href="${url}" target="_blank" download><img src="assets/pptx.png" alt="Download PPTX" style="width: 24px; height: 24px;"> Télécharger le CV</a>`);
    return this.sanitizer.bypassSecurityTrustHtml(newText);
  }

  private addMessage(text: string, sender: string): void {
    this.messages.push({text, sender});
    this.saveMessages();
    this.scrollToBottom();
  }

  private saveMessages(): void {
    sessionStorage.setItem('chatMessages', JSON.stringify(this.messages));
  }

  private loadMessages(): void {
    const messages = sessionStorage.getItem('chatMessages');
    if (messages) {
      this.messages = JSON.parse(messages);
    }
  }

  private scrollToBottom(): void {
    try {
      this.chatEnd.nativeElement.scrollIntoView({behavior: 'smooth'});
    } catch (err) {}
  }

  oncloseChatbot(): void {
    this.closeChatbot.emit();
  }

  onFileSelected(event: any): void {
    const file: File = event.target.files[0];
    if (file) {
      this.addMessage(`Fichier joint : ${file.name}`, 'user');
      this.fileAttached = true;
    }
  }
}
