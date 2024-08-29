import { Component, OnInit } from '@angular/core';
import { NgbDropdownConfig } from '@ng-bootstrap/ng-bootstrap';
import { CollabuserService } from '../../../services/collabuser.service';
import { Router } from "@angular/router";
import { MatDialog } from "@angular/material/dialog";
import { ChatbotComponent } from "../../chatbot/chatbot.component";

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
  providers: [NgbDropdownConfig]
})
export class NavbarComponent implements OnInit {
  public iconOnlyToggled = false;
  public sidebarToggled = false;
  public username: string = '';
  public profileImageUrl: string = '';

  constructor(private config: NgbDropdownConfig, private collabuserService: CollabuserService, private router: Router, private dialog: MatDialog) {
    config.placement = 'bottom-right';
  }

  ngOnInit(): void {
    this.username = this.collabuserService.getFullName();

    const userId = this.getId();
    if (userId) {
      this.profileImageUrl = `http://localhost:8000/collaborateurs/image/${userId}/`;
    }
  }
  getId(): number {
    const user = this.collabuserService.getUserData();
    return user ? user.id : null;
  }


  logout(): void {
    this.collabuserService.logout().subscribe({
      next: (response) => {
        console.log(response.message);
        this.router.navigate(['user-pages/login']); // Corrected navigation path
      },
      error: (error) => {
        console.error('Logout failed', error);
      }
    });
  }

  toggleOffcanvas(): void {
    document.querySelector('.sidebar-offcanvas').classList.toggle('active');
  }

  toggleSidebar(): void {
    let body = document.querySelector('body');
    if ((!body.classList.contains('sidebar-toggle-display')) && (!body.classList.contains('sidebar-absolute'))) {
      this.iconOnlyToggled = !this.iconOnlyToggled;
      body.classList.toggle('sidebar-icon-only', this.iconOnlyToggled);
    } else {
      this.sidebarToggled = !this.sidebarToggled;
      body.classList.toggle('sidebar-hidden', this.sidebarToggled);
    }
  }

  toggleRightSidebar(): void {
    document.querySelector('#right-sidebar').classList.toggle('open');
  }

  openChatbotModal(): void {
    const dialogRef = this.dialog.open(ChatbotComponent, {
      width: '400px',
      height: '600px',
      position: { top: '10px', left: '10px' }
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }
}
