import {Component, HostListener, OnInit} from '@angular/core';
import { Router, NavigationEnd, NavigationStart, RouteConfigLoadStart, RouteConfigLoadEnd } from '@angular/router';
import {TranslateService} from '@ngx-translate/core';
import { ChatbotPopupService } from '../services/chatbot-popup.service';
import { ChatbotComponent } from '../app/chatbot/chatbot.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit{
  title = 'demo1';
  showLayout: boolean = true;

  showSidebar: boolean = true;
  showNavbar: boolean = true;
  showFooter: boolean = true;
  showSettings: boolean = true;
  isLoading: boolean;
  displayChatbot = false;

  constructor( translate: TranslateService,private chatbotPopupService: ChatbotPopupService, private router: Router // Injection du service de dialogue
)  {

    // Removing Sidebar, Navbar, Footer for Documentation, Error and Auth pages
    router.events.forEach((event) => {
      if(event instanceof NavigationStart) {
        if(event.url === '/rtl') {
          translate.use('ar');
          document.querySelector('body').classList.add('rtl');
        } else {
          translate.use('en');
          document.querySelector('body').classList.remove('rtl');
        }
        if((event['url'] == '/user-pages/login') || (event['url'] == '/user-pages/login-2') || (event['url'] == '/user-pages/register') || (event['url'] == '/user-pages/register-2') || (event['url'] == '/user-pages/lock-screen') || (event['url'] == '/error-pages/404') || (event['url'] == '/error-pages/500') || (event['url'] == '/user-pages/reset') || (event['url'] == '/user-pages/change-password')) {
          this.showSidebar = false;
          this.showNavbar = false;
          this.showFooter = false;
          this.showSettings = false;
          document.querySelector('.main-panel').classList.add('w-100');
          document.querySelector('.page-body-wrapper').classList.add('full-page-wrapper');
          if((event['url'] == '/user-pages/login-2') || (event['url'] == '/user-pages/register-2')) {
            document.querySelector('.content-wrapper').classList.add('auth', 'auth-img-bg', );
          } else if(event['url'] == '/user-pages/lock-screen') {
            document.querySelector('.content-wrapper').classList.add('auth', 'lock-full-bg');
          } else {
            document.querySelector('.content-wrapper').classList.remove('auth', 'auth-img-bg', );
            document.querySelector('.content-wrapper').classList.remove('auth', 'lock-full-bg');
          }
          if((event['url'] == '/error-pages/404') || (event['url'] == '/error-pages/500')) {
            document.querySelector('.content-wrapper').classList.add('p-0');
          }
        } else {
          this.showSidebar = true;
          this.showNavbar = true;
          this.showFooter = true;
          this.showSettings = true;
          document.querySelector('.main-panel').classList.remove('w-100');
          document.querySelector('.page-body-wrapper').classList.remove('full-page-wrapper');
          document.querySelector('.content-wrapper').classList.remove('auth', 'auth-img-bg');
          document.querySelector('.content-wrapper').classList.remove('p-0');
        }
      }
    });

    // Spinner for lazyload modules
    router.events.forEach((event) => {
      if (event instanceof RouteConfigLoadStart) {
          this.isLoading = true;
      } else if (event instanceof RouteConfigLoadEnd) {
          this.isLoading = false;
      }
    });

  }



  ngOnInit() {
    // Scroll to top after route change
    this.router.events.subscribe((evt) => {
      if (!(evt instanceof NavigationEnd)) {
          return;
      }
      window.scrollTo(0, 0);
    });
  }
// app.component.ts
@HostListener('document:click', ['$event'])
onDocumentClick(event: MouseEvent): void {
  const chatbotElement = document.getElementById('chatbotPopup');
  if (chatbotElement && !chatbotElement.contains(event.target as Node)) {
    this.displayChatbot = false;
  }
}

  toggleChatbotPopup(): void {
    this.displayChatbot = !this.displayChatbot;  // Toggle l'état pour ouvrir/fermer le chatbot
  }

  closeChatbot(): void {
    this.displayChatbot = false; // Assurez-vous que cette méthode est correctement définie
  }



}
