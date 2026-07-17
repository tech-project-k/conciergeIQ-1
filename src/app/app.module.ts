import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';
import {PreloaderComponent} from './components/preloader/preloader.component';
import { AppRoutingModule } from './app-routing.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppComponent } from './app.component';
import { HomeComponent } from './pages/home/home.component';

import { NavbarComponent } from './components/navbar/navbar.component';
import { HeroComponent } from './components/hero/hero.component';
import { SearchBarComponent } from './components/search-bar/search-bar.component';
import { FooterComponent } from './components/footer/footer.component';
import { HotelCardComponent } from './components/hotel-card/hotel-card.component';
import { DestinationCardComponent } from './components/destination-card/destination-card.component';
import { EventCardComponent } from './components/event-card/event-card.component';
import { RestaurantCardComponent } from './components/restaurant-card/restaurant-card.component';
import { ReviewCardComponent } from './components/review-card/review-card.component';
@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    NavbarComponent,
    HeroComponent,
    SearchBarComponent,
    FooterComponent,
    HotelCardComponent,
    DestinationCardComponent,
    EventCardComponent,
    RestaurantCardComponent,
    ReviewCardComponent,
    PreloaderComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    CommonModule,
    BrowserAnimationsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }