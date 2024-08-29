import { Component, OnInit } from '@angular/core';
import { CollabuserService } from '../../../services/collabuser.service';  // Adjust path as necessary

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {
  public uiBasicCollapsed = false;
  public uiAdvancedCollapsed = false;
  public formsCollapsed = false;
  public editorsCollapsed = false;
  public chartsCollapsed = false;
  public tablesCollapsed = false;
  public iconsCollapsed = false;
  public mapsCollapsed = false;
  public userPagesCollapsed = false;
  public errorCollapsed = false;
  public generalPagesCollapsed = false;
  public eCommerceCollapsed = false;
    public username: string = '';
public role : string = '' ;
  public profileImageUrl: string = '';
    isBasicUIVisible = false;
  isFormElementsVisible = false;
  isChartsVisible = false;
  isIconsVisible = false;
  isUserPagesVisible = false;
  isDocumentationVisible = false;

  poste: string = '';

  constructor( private collabuserService: CollabuserService) {  this.isBasicUIVisible = false;   // Hide Basic UI Elements
    this.isFormElementsVisible = false; // Hide Form Elements
    this.isChartsVisible = false;    // Hide Charts
    this.isIconsVisible = false;     // Hide Icons
    this.isUserPagesVisible = false; // Hide User Pages
    this.isDocumentationVisible = false; }

  ngOnInit() {
    const body = document.querySelector('body');

    // add class 'hover-open' to sidebar navitem while hover in sidebar-icon-only menu
    document.querySelectorAll('.sidebar .nav-item').forEach(function (el) {
      el.addEventListener('mouseover', function() {
        if(body.classList.contains('sidebar-icon-only')) {
          el.classList.add('hover-open');
        }
      });
      el.addEventListener('mouseout', function() {
        if(body.classList.contains('sidebar-icon-only')) {
          el.classList.remove('hover-open');
        }
      });
    });
        this.username = this.collabuserService.getFullName();
        this.role = this.collabuserService.getPoste();
            const userId = this.collabuserService.getId();

    if (userId) {
      this.profileImageUrl = `http://localhost:8000/collaborateurs/image/${userId}/`;
    }

    const user = JSON.parse(sessionStorage.getItem('user'));
    if (user) {
      this.poste = user.poste;
    }
  }



  // Méthode pour vérifier les postes
  hasAccessToAll(): boolean {
    return this.poste !== 'Junior Consultant' && this.poste !== 'Senior Consultant';
  }
}


