import { Component, OnInit } from '@angular/core';
import { ChartType } from 'chart.js';
import { MultiDataSet, Label, Colors } from 'ng2-charts';
import { CollabuserService } from '../../services/collabuser.service';
import {ScrapeService} from "../../services/scrape.service";
import {NgbModal, NgbModalRef} from "@ng-bootstrap/ng-bootstrap";  // Adjust path as necessary

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class DashboardComponent implements OnInit {
public users: any[] = [];
  public scrapingData: any = null;
public actu: any[] = [];
  public currentPage: number = 0;
  public pageSize: number = 5;
  private modalRef: NgbModalRef;
  public selectedUser: any = {};  // Object to hold selected user data for editing

  toggleProBanner(event) {
    event.preventDefault();
    document.querySelector('body').classList.toggle('removeProbanner');
  }
    public username: string = '';

  constructor(private collabuserService: CollabuserService , private scrapeService: ScrapeService ,    private modalService: NgbModal
) { }

  ngOnInit() {
    this.username = this.collabuserService.getFullName();

    this.loadScrapingData();
    this.loadActu();
        const userId = this.collabuserService.getId();
    this.loadUsers();


  }
loadActu() {
  this.scrapeService.getActu().subscribe(
    data => {
      console.log('Data :', data);  // Check the structure of the data
      this.actu = data;
    },
    error => {
      console.error('Error loading scraping data:', error);
    }
  );
}
  loadUsers() {
    this.collabuserService.getAllUsers().subscribe(
      data => {
        this.users = data;  // Store the users data returned from the server
      },
      error => {
        console.error('Error loading users:', error);
      }
    );
  }

  nextPage() {
    const nextPage = this.currentPage + 1;
    const startIndex = nextPage * this.pageSize;
    if (startIndex < this.actu.length) {
      this.currentPage = nextPage;
    }
  }

  previousPage() {
    const previousPage = this.currentPage - 1;
    if (previousPage >= 0) {
      this.currentPage = previousPage;
    }
  }

  // Helper to slice the array of articles for display
  get displayedArticles() {
    if (this.actu && this.actu.length > 0) {
      const startIndex = this.currentPage * this.pageSize;
      return this.actu.slice(startIndex, startIndex + this.pageSize);
    } else {
      return [];  // Return an empty array if actu is undefined or empty
    }
  }


  loadScrapingData() {
    this.scrapeService.getScrapingData().subscribe(
      data => {
        this.scrapingData = data;
      },
      error => {
        console.error('Error loading scraping data:', error);
      }
    );
  }



getImageUrl(userId: number): string {
  return `http://localhost:8000/collaborateurs/image/${userId}/`;
}

  public doughnutChartLabels: Label[] = ["Paypal", "Stripe","Cash"];
  public doughnutChartData: MultiDataSet = [
    [55, 25, 20]
  ];
  public doughnutChartColors: Colors[] = [
    {
      backgroundColor: [
        '#111111',
        '#00d25b',
        '#ffab00'
      ]
    }
  ];
  public doughnutChartType: ChartType = 'doughnut';
  public doughnutChartChartPlugins = {
    beforeDraw: function(chart) {
      var width = chart.chart.width,
          height = chart.chart.height,
          ctx = chart.chart.ctx;

      ctx.restore();
      var fontSize = 1;
      ctx.font = fontSize + "rem sans-serif";
      ctx.textAlign = 'left';
      ctx.textBaseline = "middle";
      ctx.fillStyle = "#ffffff";

      var text = "$1200",
          textX = Math.round((width - ctx.measureText(text).width) / 2),
          textY = height / 2.4;

      ctx.fillText(text, textX, textY);

      ctx.restore();
      var fontSize = 0.75;
      ctx.font = fontSize + "rem sans-serif";
      ctx.textAlign = 'left';
      ctx.textBaseline = "middle";
      ctx.fillStyle = "#6c7293";

      var texts = "Total",
          textsX = Math.round((width - ctx.measureText(text).width) / 1.93),
          textsY = height / 1.7;

      ctx.fillText(texts, textsX, textsY);
      ctx.save();
    }
  }
  public doughnutChartOptions: any = {
    responsive: true,
    cutoutPercentage: 70,
    maintainAspectRatio: true,
    segmentShowStroke: false,
    elements: {
      arc: {
          borderWidth: 0
      }
    },
    legend: {
      display: false,
    }
  };

  portfolioCarousel = {
    loop: true,
    dots: false,
    margin: 10,
    items: 1,
    nav: true,
    autoplay: true,
    autoplayTimeout: 5500,
    navText: ["<i class='mdi mdi-chevron-left'></i>", "<i class='mdi mdi-chevron-right'></i>"]
  }

mapStyle = {
  sources: {
    world: {
      type: "geojson",
      data: "assets/countries.geo.json"
    }
  },
   version: 8,
  layers: [{
    "id": "countries",
    "type": "fill",
    "source": "world",
    "layout": {},
    "paint": {
      'fill-color': [
        'match',
        ['get', 'id'],
        'USA', '#FFFF00',
        'CAN', '#FFFF00',
        'BRA', '#FFFF00',
        'ARG', '#FFFF00',
        'VEN', '#FFFF00',
        'MEX', '#FFFF00',
        // Add more countries as needed
        '#DDDDDD'   // Default color for others
      ]
    }
  }]
};




  openEditModal(content, user) {
  this.selectedUser = { ...user };  // Copy user data to selectedUser
  this.modalRef = this.modalService.open(content, { windowClass: 'custom-modal', ariaLabelledBy: 'modal-basic-title' });
}

  editUser() {
    const userId = this.selectedUser.id;
                const userId1 = this.collabuserService.getId();

    const userData = {
      poste: this.selectedUser.poste,
      competences: this.selectedUser.competences,
      diplome_obtenu: this.selectedUser.diplome_obtenu,
      institution: this.selectedUser.institution,
      date: this.selectedUser.date
    };

    this.collabuserService.editUser(userId, userData).subscribe(
      response => {
        console.log('Utilisateur mis à jour avec succès', response);
        this.modalRef.close();  // Close the modal on success
        this.loadUsers();  // Reload users to see the changes
      },
      error => {
        console.error('Erreur lors de la mise à jour de l\'utilisateur', error);
      }
    );
  }
    openDeleteModal(content, user) {
    this.selectedUser = { ...user };  // Copy user data to selectedUser
    this.modalRef = this.modalService.open(content, { windowClass: 'custom-modal', ariaLabelledBy: 'modal-basic-title' });
  }

  confirmDelete() {
    const userId = this.selectedUser.id;
            const userId1 = this.collabuserService.getId();

    this.collabuserService.deleteUser(userId).subscribe(
      response => {
        console.log('Utilisateur supprimé avec succès', response);
        this.modalRef.close();  // Close the modal on success
        this.loadUsers();  // Reload users to see the changes
      },
      error => {
        console.error('Erreur lors de la suppression de l\'utilisateur', error);
      }
    );
  }

}
