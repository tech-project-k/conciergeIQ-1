package com.conciergeiq.controller;

import com.conciergeiq.model.Guest;
import com.conciergeiq.model.Preference;
import com.conciergeiq.repository.GuestRepository;
import com.conciergeiq.repository.PreferenceRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/auth")
@CrossOrigin(origins = "*")
public class GuestController {

    @Autowired
    private GuestRepository guestRepository;

    @Autowired
    private PreferenceRepository preferenceRepository;

    private Guest getOrCreateDefaultGuest() {
        Optional<Guest> guestOpt = guestRepository.findByEmail("default@conciergeiq.com");
        if (guestOpt.isPresent()) {
            return guestOpt.get();
        }
        
        Guest guest = Guest.builder()
            .email("default@conciergeiq.com")
            .roomNumber("Room 404")
            .fullName("Default Traveler")
            .build();
        guest = guestRepository.save(guest);

        Preference pref = Preference.builder()
            .guest(guest)
            .travelStyle("{\"adventure\":3,\"nature\":3,\"luxury\":3}")
            .dietaryRestrictions("")
            .accessibilityNeeds("")
            .budgetTier("moderate")
            .build();
        preferenceRepository.save(pref);

        guest.setPreference(pref);
        return guest;
    }

    @GetMapping("/me")
    public Guest getMe() {
        return getOrCreateDefaultGuest();
    }

    @PutMapping("/preferences")
    public Preference updatePreferences(@RequestBody Map<String, Object> payload) {
        Guest guest = getOrCreateDefaultGuest();
        Preference pref = guest.getPreference();
        if (pref == null) {
            pref = Preference.builder().guest(guest).build();
        }

        if (payload.containsKey("budget_tier")) {
            pref.setBudgetTier((String) payload.get("budget_tier"));
        }
        
        // Handle serialization lists / style maps
        if (payload.containsKey("travel_style")) {
            pref.setTravelStyle(payload.get("travel_style").toString());
        }
        if (payload.containsKey("dietary_restrictions")) {
            pref.setDietaryRestrictions(payload.get("dietary_restrictions").toString());
        }
        if (payload.containsKey("accessibility_needs")) {
            pref.setAccessibilityNeeds(payload.get("accessibility_needs").toString());
        }

        return preferenceRepository.save(pref);
    }
}
