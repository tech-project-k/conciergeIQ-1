package com.conciergeiq.controller;

import com.conciergeiq.model.Guest;
import com.conciergeiq.repository.GuestRepository;
import com.conciergeiq.service.ChatOrchestratorService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.*;

@RestController
@RequestMapping("/chat")
@CrossOrigin(origins = "*")
public class ChatController {

    @Autowired
    private ChatOrchestratorService chatOrchestratorService;

    @Autowired
    private GuestRepository guestRepository;

    private Guest getDefaultGuest() {
        return guestRepository.findByEmail("default@conciergeiq.com")
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Default guest not initialized"));
    }

    @PostMapping
    public Map<String, Object> chat(@RequestBody Map<String, Object> payload) {
        String query = (String) payload.get("query");
        if (query == null || query.trim().isEmpty()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Query cannot be empty");
        }

        UUID tripId = null;
        if (payload.containsKey("trip_id") && payload.get("trip_id") != null) {
            try {
                tripId = UUID.fromString((String) payload.get("trip_id"));
            } catch (IllegalArgumentException e) {
                // Ignore invalid UUID
            }
        }

        Guest guest = getDefaultGuest();
        Map<String, Object> result = chatOrchestratorService.handleChat(query, tripId, guest);

        // Keep a simple mock messages list representation to fit React frontend history
        List<Map<String, String>> messagesList = new ArrayList<>();
        messagesList.add(Map.of("role", "user", "content", query, "id", UUID.randomUUID().toString()));
        messagesList.add(Map.of("role", "assistant", "content", (String) result.get("response_text"), "id", UUID.randomUUID().toString()));
        
        result.put("messages", messagesList);
        return result;
    }

    @GetMapping("/history/{tripId}")
    public List<Map<String, String>> chatHistory(@PathVariable UUID tripId) {
        // Return a default welcome message to satisfy initial loading request
        return List.of(
            Map.of("role", "assistant", "content", "Welcome back! What afternoon changes would you like to make to your itinerary? I will utilize OpenClaw to book tickets and verify conflict reservations.", "id", "init-welcome")
        );
    }
}
