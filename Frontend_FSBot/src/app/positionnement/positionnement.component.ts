import { Component, OnInit } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-positionnement',
  templateUrl: './positionnement.component.html',
  styleUrls: ['./positionnement.component.scss']
})
export class PositionnementComponent implements OnInit {
  safeUrl: SafeResourceUrl;

  constructor(private sanitizer: DomSanitizer) { }

  ngOnInit(): void {
    const iframeUrl = 'https://app.powerbi.com/reportEmbed?reportId=dc345a72-241d-4379-bfe8-a62b39b6736f&autoAuth=true&ctid=5b973f99-77df-4beb-b27d-aa0c70b8482c&filterPaneEnabled=false&navContentPaneEnabled=false';
    this.safeUrl = this.sanitizer.bypassSecurityTrustResourceUrl(iframeUrl);
  }
}
