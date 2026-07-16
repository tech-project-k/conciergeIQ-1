package com.conciergeiq.repository;

import com.conciergeiq.model.Trip;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.UUID;

@Repository
public interface TripRepository extends JpaRepository<Trip, UUID> {
    List<Trip> findByGuestIdOrderByCreatedAtDesc(UUID guestId);
    List<Trip> findByGuestIdAndStatus(UUID guestId, String status);
}
