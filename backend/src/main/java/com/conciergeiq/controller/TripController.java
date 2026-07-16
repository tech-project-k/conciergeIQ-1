package com.conciergeiq.controller;

import com.conciergeiq.model.Activity;
import com.conciergeiq.model.Guest;
import com.conciergeiq.model.Trip;
import com.conciergeiq.repository.ActivityRepository;
import com.conciergeiq.repository.GuestRepository;
import com.conciergeiq.repository.TripRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/trips")
@CrossOrigin(origins = "*")
public class TripController {

    @Autowired
    private TripRepository tripRepository;

    @Autowired
    private GuestRepository guestRepository;

    @Autowired
    private ActivityRepository activityRepository;

    private Guest getDefaultGuest() {
        return guestRepository.findByEmail("default@conciergeiq.com")
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Default guest not initialized"));
    }

    @GetMapping
    public List<Trip> listTrips() {
        Guest guest = getDefaultGuest();
        return tripRepository.findByGuestIdOrderByCreatedAtDesc(guest.getId());
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Trip createTrip(@RequestBody Trip trip) {
        Guest guest = getDefaultGuest();
        trip.setGuest(guest);
        return tripRepository.save(trip);
    }

    @GetMapping("/{tripId}")
    public Trip getTrip(@PathVariable UUID tripId) {
        Guest guest = getDefaultGuest();
        Trip trip = tripRepository.findById(tripId)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Trip not found"));
            
        if (!trip.getGuest().getId().equals(guest.getId())) {
            throw new ResponseStatusException(HttpStatus.FORBIDDEN, "Access denied");
        }
        
        // Fetch activities and attach
        List<Activity> activities = activityRepository.findByTripIdOrderByDayNumberAscStartTimeAsc(tripId);
        trip.setActivities(activities);
        return trip;
    }

    @PutMapping("/{tripId}")
    public Trip updateTrip(@PathVariable UUID tripId, @RequestBody Trip tripIn) {
        Trip trip = tripRepository.findById(tripId)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Trip not found"));
            
        if (tripIn.getDestination() != null) trip.setDestination(tripIn.getDestination());
        if (tripIn.getStartDate() != null) trip.setStartDate(tripIn.getStartDate());
        if (tripIn.getEndDate() != null) trip.setEndDate(tripIn.getEndDate());
        if (tripIn.getStatus() != null) trip.setStatus(tripIn.getStatus());

        return tripRepository.save(trip);
    }

    @DeleteMapping("/{tripId}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteTrip(@PathVariable UUID tripId) {
        Trip trip = tripRepository.findById(tripId)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Trip not found"));
        tripRepository.delete(trip);
    }

    @PostMapping("/{tripId}/activities")
    public Activity addActivity(@PathVariable UUID tripId, @RequestBody Activity activity) {
        Trip trip = tripRepository.findById(tripId)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Trip not found"));
        activity.setTrip(trip);
        return activityRepository.save(activity);
    }
}
