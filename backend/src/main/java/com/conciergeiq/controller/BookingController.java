package com.conciergeiq.controller;

import com.conciergeiq.model.Booking;
import com.conciergeiq.service.OpenClawService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/bookings")
@CrossOrigin(origins = "*")
public class BookingController {

    @Autowired
    private OpenClawService openClawService;

    @PostMapping
    public Booking createBooking(@RequestBody Map<String, String> payload) {
        String tripIdStr = payload.get("trip_id");
        String activityIdStr = payload.get("activity_id");

        if (tripIdStr == null || activityIdStr == null) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "trip_id and activity_id are required");
        }

        try {
            UUID tripId = UUID.fromString(tripIdStr);
            UUID activityId = UUID.fromString(activityIdStr);
            return openClawService.secureBooking(tripId, activityId);
        } catch (IllegalArgumentException e) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Invalid UUID format");
        }
    }
}
