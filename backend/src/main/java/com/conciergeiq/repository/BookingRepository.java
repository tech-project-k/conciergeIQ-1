package com.conciergeiq.repository;

import com.conciergeiq.model.Booking;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface BookingRepository extends JpaRepository<Booking, UUID> {
    List<Booking> findByTripId(UUID tripId);
    Optional<Booking> findByActivityId(UUID activityId);
}
