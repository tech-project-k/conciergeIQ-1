package com.conciergeiq.controller;

import com.conciergeiq.model.ChatMessage;
import com.conciergeiq.model.Guest;
import com.conciergeiq.model.Trip;
import com.conciergeiq.repository.ChatMessageRepository;
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

    @Autowired
    private ChatMessageRepository chatMessageRepository;

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

        // Fetch actual trip ID that was processed/created
        Trip trip = (Trip) result.get("trip");
        UUID actualTripId = trip != null ? trip.getId() : (tripId != null ? tripId : UUID.fromString("00000000-0000-0000-0000-000000000000"));

        // Save User Query
        chatMessageRepository.save(ChatMessage.builder()
            .tripId(actualTripId)
            .role("user")
            .content(query)
            .build());

        // Save Assistant Response
        chatMessageRepository.save(ChatMessage.builder()
            .tripId(actualTripId)
            .role("assistant")
            .content((String) result.get("response_text"))
            .build());

        // Load entire history
        List<ChatMessage> dbMessages = chatMessageRepository.findByTripIdOrderByCreatedAtAsc(actualTripId);
        List<Map<String, String>> messagesList = new ArrayList<>();
        for (ChatMessage msg : dbMessages) {
            messagesList.add(Map.of(
                "role", msg.getRole(),
                "content", msg.getContent(),
                "id", msg.getId().toString()
            ));
        }
        
        result.put("messages", messagesList);
        return result;
    }

    @GetMapping("/history/{tripId}")
    public List<Map<String, String>> chatHistory(@PathVariable UUID tripId) {
        List<ChatMessage> dbMessages = chatMessageRepository.findByTripIdOrderByCreatedAtAsc(tripId);
        if (dbMessages.isEmpty()) {
            // Auto-save initial welcome message
            ChatMessage welcome = ChatMessage.builder()
                .tripId(tripId)
                .role("assistant")
                .content("Welcome back! What afternoon changes would you like to make to your itinerary? I will utilize OpenClaw to book tickets and verify conflict reservations.")
                .build();
            chatMessageRepository.save(welcome);
            dbMessages = List.of(welcome);
        }

        List<Map<String, String>> messagesList = new ArrayList<>();
        for (ChatMessage msg : dbMessages) {
            messagesList.add(Map.of(
                "role", msg.getRole(),
                "content", msg.getContent(),
                "id", msg.getId().toString()
            ));
        }
        return messagesList;
    }
}
