import { Component } from '@angular/core';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent {
  user = {
    name: 'Maya Chen',
    email: 'maya@conciergeiq.com',
    location: 'Dubai, UAE',
    status: 'Premium Traveler'
  };

  trips = [
    { title: 'Alpine Escape', date: 'Sep 2025', tag: 'Completed' },
    { title: 'Coastal Retreat', date: 'Oct 2025', tag: 'Planned' },
    { title: 'Desert Adventure', date: 'Nov 2025', tag: 'In Progress' }
  ];
}
