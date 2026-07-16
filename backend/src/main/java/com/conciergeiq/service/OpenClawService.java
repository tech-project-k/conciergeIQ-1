package com.conciergeiq.service;

import com.conciergeiq.model.Activity;
import com.conciergeiq.model.Booking;
import com.conciergeiq.repository.ActivityRepository;
import com.conciergeiq.repository.BookingRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;
import java.util.UUID;

@Service
public class OpenClawService {

    @Autowired
    private BookingRepository bookingRepository;

    @Autowired
    private ActivityRepository activityRepository;

    /**
     * Secures booking confirmations using OpenClaw agent tools.
     * Interacts with simulated external reservation APIs.
     */
    @Transactional
    public Booking secureBooking(UUID tripId, UUID activityId) {
        Optional<Activity> activityOpt = activityRepository.findById(activityId);
        if (activityOpt.isEmpty()) {
            throw new IllegalArgumentException("Activity not found: " + activityId);
        }
        Activity activity = activityOpt.get();

        // 1. Simulate external ticketing API delay and connection call
        String confCode = "CLAW-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
        
        // 2. Check if a booking already exists
        Optional<Booking> bookingOpt = bookingRepository.findByActivityId(activityId);
        Booking booking;
        if (bookingOpt.isPresent()) {
            booking = bookingOpt.get();
            booking.setStatus("confirmed");
            booking.setExternalConfirmationCode(confCode);
        } else {
            booking = Booking.builder()
                .tripId(tripId)
                .activityId(activityId)
                .status("confirmed")
                .externalConfirmationCode(confCode)
                .pricePaid(activity.getCost())
                .build();
        }

        // 3. Save to database
        booking = bookingRepository.save(booking);

        // 4. Update parent activity confirmation link
        activity.setBookingConfirmationCode(confCode);
        activityRepository.save(activity);

        return booking;
    }
}
