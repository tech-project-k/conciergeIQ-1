import { AfterViewInit, Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-hero',
  templateUrl: './hero.component.html',
  styleUrls: ['./hero.component.css']
})
export class HeroComponent implements AfterViewInit {

  constructor(private router: Router) {}

  ngAfterViewInit(): void {
    const video = document.getElementById('bgVideo') as HTMLVideoElement;

    if (video) {
      video.muted = true;
      video.defaultMuted = true;

      video.play()
        .then(() => console.log('Video Playing'))
        .catch(err => console.log(err));
    }
  }

  goToLogin() {
    this.router.navigate(['/login']);
  }

  goToMap() {
    this.router.navigate(['/map']);
  }
}