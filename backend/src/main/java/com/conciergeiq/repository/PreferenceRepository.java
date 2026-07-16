package com.conciergeiq.repository;

import com.conciergeiq.model.Preference;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.UUID;

@Repository
public interface PreferenceRepository extends JpaRepository<Preference, UUID> {
    void deleteByGuestId(UUID guestId);
}
