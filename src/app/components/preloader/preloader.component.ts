import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-preloader',
  templateUrl: './preloader.component.html',
  styleUrls: ['./preloader.component.css']
})
export class PreloaderComponent implements OnInit {

  showLoader = true;

  ngOnInit(): void {

    setTimeout(() => {

      this.showLoader = false;

    },2500);

  }

}