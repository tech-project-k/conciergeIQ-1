import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CommonModule } from '@angular/common';

import { AppRoutingModule } from './app-routing.module';

import { AppComponent } from './app.component';

import { NavbarComponent } from './components/navbar/navbar.component';
import { HeroComponent } from './components/hero/hero.component';
import { SearchBarComponent } from './components/search-bar/search-bar.component';
import { HotelCardComponent } from './components/hotel-card/hotel-card.component';
import { DestinationCardComponent } from './components/destination-card/destination-card.component';
import { RestaurantCardComponent } from './components/restaurant-card/restaurant-card.component';
import { EventCardComponent } from './components/event-card/event-card.component';
import { ReviewCardComponent } from './components/review-card/review-card.component';
import { ContactComponent } from './components/contact/contact.component';
import { FooterComponent } from './components/footer/footer.component';
import { LoginComponent } from './components/login/login.component';
import { AiChatComponent } from './components/ai-chat/ai-chat.component';
import { PreloaderComponent } from './components/preloader/preloader.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { ProfileComponent } from './components/profile/profile.component';

import { HomeComponent } from './pages/home/home.component';
import { MapPageComponent } from './pages/map-page/map-page.component';

@NgModule({
  declarations: [
    AppComponent,

    NavbarComponent,
    HeroComponent,
    SearchBarComponent,
    HotelCardComponent,
    DestinationCardComponent,
    RestaurantCardComponent,
    EventCardComponent,
    ReviewCardComponent,
    ContactComponent,
    FooterComponent,
    LoginComponent,
    AiChatComponent,
    PreloaderComponent,
    DashboardComponent,
    ProfileComponent,

    HomeComponent,
    MapPageComponent
  ],

  imports: [
    BrowserModule,
    CommonModule,
    BrowserAnimationsModule,
    AppRoutingModule
  ],

  providers: [],

  bootstrap: [AppComponent]

})
export class AppModule { }