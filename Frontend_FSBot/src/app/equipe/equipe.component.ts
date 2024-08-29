import { Component, OnInit } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-equipe',
  templateUrl: './equipe.component.html',
  styleUrls: ['./equipe.component.scss']
})
export class EquipeComponent implements OnInit {

  safeUrl: SafeResourceUrl;

  constructor(private sanitizer: DomSanitizer) { }

  ngOnInit(): void {
    const iframeUrl = 'https://app.powerbi.com/reportEmbed?reportId=71cd6782-fd9a-47ab-8ab2-fec5c4fbc793&autoAuth=true&ctid=5b973f99-77df-4beb-b27d-aa0c70b8482c&filterPaneEnabled=false&navContentPaneEnabled=false';
    this.safeUrl = this.sanitizer.bypassSecurityTrustResourceUrl(iframeUrl);
  }
}
