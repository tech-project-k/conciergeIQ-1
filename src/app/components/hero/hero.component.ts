import { AfterViewInit, Component } from '@angular/core';

@Component({
  selector: 'app-hero',
  templateUrl: './hero.component.html',
  styleUrls: ['./hero.component.css']
})
export class HeroComponent implements AfterViewInit {

  ngAfterViewInit(): void {

    const video = document.getElementById('bgVideo') as HTMLVideoElement;

    video.muted = true;
    video.defaultMuted = true;

    video.play().then(() => {
      console.log('Video Playing');
    }).catch((err) => {
      console.log(err);
    });

  }

}