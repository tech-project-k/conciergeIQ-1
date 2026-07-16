package com.conciergeiq.service;

import com.conciergeiq.model.*;
import com.conciergeiq.repository.*;
import dev.langchain4j.model.openai.OpenAiChatModel;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.*;

@Service
public class ChatOrchestratorService {

    @Autowired
    private GuestRepository guestRepository;

    @Autowired
    private TripRepository tripRepository;

    @Autowired
    private ActivityRepository activityRepository;

    @Autowired
    private BookingRepository bookingRepository;

    @Autowired
    private VectorSearchService vectorSearchService;

    @Value("${openai.api.key}")
    private String apiKey;

    @Value("${openai.api.base}")
    private String apiBase;

    // Direct mock coordinates
    private static final Map<String, double[]> CITY_COORDS = Map.of(
        "paris", new double[]{48.8566, 2.3522},
        "tokyo", new double[]{35.6762, 139.6503}
    );

    @Transactional
    public Map<String, Object> handleChat(String query, UUID tripId, Guest guest) {
        String cleanQuery = query.toLowerCase();
        Map<String, Object> response = new HashMap<>();
        List<String> warnings = new ArrayList<>();
        
        // Detect Intent
        String intent = "chat";
        if (cleanQuery.contains("plan") || cleanQuery.contains("trip") || cleanQuery.contains("visit") || cleanQuery.contains("travel")) {
            intent = "plan";
        } else if (cleanQuery.contains("change") || cleanQuery.contains("move") || cleanQuery.contains("replace") || cleanQuery.contains("add") || cleanQuery.contains("avoid")) {
            intent = "modify";
        }
        
        // Load active trip
        Trip activeTrip = null;
        if (tripId != null) {
            activeTrip = tripRepository.findById(tripId).orElse(null);
        }
        if (activeTrip == null) {
            List<Trip> planningTrips = tripRepository.findByGuestIdAndStatus(guest.getId(), "planning");
            if (!planningTrips.isEmpty()) {
                activeTrip = planningTrips.get(0);
            }
        }
        
        // 1. EXECUTE INTENT NODE
        String destination = activeTrip != null ? activeTrip.getDestination() : "Paris";
        if (cleanQuery.contains("tokyo")) {
            destination = "Tokyo";
        } else if (cleanQuery.contains("paris")) {
            destination = "Paris";
        }

        // 2. RAG RETRIEVAL NODE
        List<Map<String, String>> localEvents = vectorSearchService.search(query, destination);
        
        // 3. EXECUTE PLANNING NODE
        String responseText = "";
        List<Activity> activities = new ArrayList<>();
        
        if (intent.equals("plan") || activeTrip == null) {
            // Plan a new trip
            LocalDate start = LocalDate.now();
            LocalDate end = start.plusDays(2);
            long days = ChronoUnit.DAYS.between(start, end) + 1;
            
            if (activeTrip != null) {
                // Delete old activities
                activityRepository.deleteByTripId(activeTrip.getId());
                activeTrip.setDestination(destination);
                activeTrip.setStartDate(start);
                activeTrip.setEndDate(end);
                activeTrip = tripRepository.save(activeTrip);
            } else {
                activeTrip = Trip.builder()
                    .guest(guest)
                    .destination(destination)
                    .startDate(start)
                    .endDate(end)
                    .status("planning")
                    .build();
                activeTrip = tripRepository.save(activeTrip);
            }
            
            // Build activities
            activities = generateItinerary(activeTrip, (int) days, destination, localEvents);
            activityRepository.saveAll(activities);
            activeTrip.setActivities(activities);
            
            responseText = "I've drafted a personalized guest itinerary for your trip to " + destination + "! I searched local event reviews in OpenSearch and scheduled activities like " + (localEvents.isEmpty() ? "sightseeing" : localEvents.get(0).get("name")) + ". Let me know if you would like me to modify anything.";
            
        } else if (intent.equals("modify") && activeTrip != null) {
            // Modify itinerary
            activities = activityRepository.findByTripIdOrderByDayNumberAscStartTimeAsc(activeTrip.getId());
            
            if (cleanQuery.contains("dinner") && (cleanQuery.contains("move") || cleanQuery.contains("tomorrow"))) {
                // Move dinner to next day
                for (Activity act : activities) {
                    if (act.getType().equals("dinner") && act.getDayNumber() == 1) {
                        act.setDayNumber(2);
                        act.setStartTime("20:00");
                        act.setEndTime("22:00");
                        act.setDescription("[Modified] Moved dinner to day 2");
                        warnings.add("Dinner moved to Day 2. Please double check conflict reservations.");
                    }
                }
                activityRepository.saveAll(activities);
            }
            
            responseText = "I've updated your schedule according to your request! Dinner has been shifted, and I've re-optimized the transit coordinates. Let me know if the updated route looks good.";
        } else {
            // Chat
            responseText = "I am your Concierge assistant. I can update your itinerary, book tickets, check conflicts, or suggest local activities. What would you like to plan?";
        }
        
        // 4. ROUTE OPTIMIZATION NODE (Haversine & travel durations)
        optimizeItinerary(activities, destination, warnings);
        activityRepository.saveAll(activities);
        
        // 5. TRIGGER LANGCHAIN4J LLM WRAPPER IF API KEY EXISTS
        if (apiKey != null && !apiKey.isEmpty()) {
            try {
                OpenAiChatModel model = OpenAiChatModel.builder()
                    .apiKey(apiKey)
                    .baseUrl(apiBase)
                    .temperature(0.2)
                    .build();
                String llmPrompt = "You are a hotel concierge. Guest request: \"" + query + "\". Current schedule details: " + responseText + ". Respond with a warm, helpful concierge text under 3 sentences.";
                String result = model.generate(llmPrompt);
                if (result != null && !result.trim().isEmpty()) {
                    responseText = result;
                }
            } catch (Exception e) {
                // Fallback silently to rule-based responseText
            }
        }
        
        response.put("response_text", responseText);
        response.put("trip", activeTrip);
        response.put("warnings", warnings);
        response.put("intent", intent);
        return response;
    }

    private List<Activity> generateItinerary(Trip trip, int days, String city, List<Map<String, String>> events) {
        List<Activity> list = new ArrayList<>();
        double[] coords = CITY_COORDS.getOrDefault(city.toLowerCase(), new double[]{48.8566, 2.3522});
        
        String hotelName = city + " Grand Hotel Resort";
        
        for (int d = 1; d <= days; d++) {
            // 1. Hotel Departure
            list.add(Activity.builder()
                .trip(trip)
                .dayNumber(d)
                .name("Hotel Departure: " + hotelName)
                .type("hotel")
                .startTime("08:30")
                .endTime("09:00")
                .latitude(coords[0])
                .longitude(coords[1])
                .address("10 Luxury Blvd, " + city)
                .cost(0.0)
                .description("Depart from your hotel.")
                .build());
                
            // 2. Morning Attraction
            list.add(Activity.builder()
                .trip(trip)
                .dayNumber(d)
                .name(city + " Historic Square")
                .type("attraction")
                .startTime("09:30")
                .endTime("12:00")
                .latitude(coords[0] + 0.005)
                .longitude(coords[1] - 0.005)
                .address("Center Plaza, " + city)
                .cost(15.0)
                .description("Explore monuments and local guide tour.")
                .build());
                
            // 3. Lunch Bistro
            list.add(Activity.builder()
                .trip(trip)
                .dayNumber(d)
                .name("La Gastronomique " + city)
                .type("lunch")
                .startTime("12:30")
                .endTime("14:00")
                .latitude(coords[0] + 0.003)
                .longitude(coords[1] + 0.001)
                .address("12 Food St, " + city)
                .cost(25.0)
                .description("Enjoy authentic regional recipes.")
                .build());
                
            // 4. Afternoon Event (From OpenSearch RAG results)
            String eventName = city + " Event Sights";
            String eventDesc = "Explore cultural events and exhibits.";
            if (events.size() >= d) {
                eventName = events.get(d - 1).get("name");
                eventDesc = events.get(d - 1).get("details");
            }
            
            list.add(Activity.builder()
                .trip(trip)
                .dayNumber(d)
                .name(eventName)
                .type("event")
                .startTime("14:30")
                .endTime("17:00")
                .latitude(coords[0] - 0.008)
                .longitude(coords[1] + 0.004)
                .address("Venue Hall, " + city)
                .cost(35.0)
                .description(eventDesc)
                .build());

            // 5. Dinner
            list.add(Activity.builder()
                .trip(trip)
                .dayNumber(d)
                .name("Chic Dining Rooms")
                .type("dinner")
                .startTime("19:00")
                .endTime("21:00")
                .latitude(coords[0] - 0.001)
                .longitude(coords[1] - 0.002)
                .address("5 Main Plaza, " + city)
                .cost(45.0)
                .description("Fine table dinner service.")
                .build());

            // 6. Return to Hotel
            list.add(Activity.builder()
                .trip(trip)
                .dayNumber(d)
                .name("Return to " + hotelName)
                .type("hotel")
                .startTime("21:30")
                .endTime("22:00")
                .latitude(coords[0])
                .longitude(coords[1])
                .address("10 Luxury Blvd, " + city)
                .cost(0.0)
                .description("End of day. Rest at hotel.")
                .build());
        }
        return list;
    }

    private void optimizeItinerary(List<Activity> list, String city, List<String> warnings) {
        if (list == null || list.isEmpty()) return;
        
        // Group by day and sort by start time
        list.sort(Comparator.comparing(Activity::getDayNumber).thenComparing(Activity::getStartTime));
        
        for (int i = 0; i < list.size(); i++) {
            Activity act = list.get(i);
            if (i == 0 || act.getDayNumber() != list.get(i - 1).getDayNumber()) {
                act.setTravelDistanceKm(0.0);
                act.setTravelDurationMin(0.0);
                act.setTravelMode("walking");
            } else {
                Activity prev = list.get(i - 1);
                if (act.getLatitude() != null && prev.getLatitude() != null) {
                    double dist = haversine(prev.getLatitude(), prev.getLongitude(), act.getLatitude(), act.getLongitude());
                    act.setTravelDistanceKm(Math.round(dist * 100.0) / 100.0);
                    
                    String mode = dist > 2.0 ? "driving" : (dist > 0.5 ? "transit" : "walking");
                    act.setTravelMode(mode);
                    
                    double speed = mode.equals("driving") ? 35.0 : (mode.equals("transit") ? 20.0 : 4.5);
                    double durationMin = (dist / speed) * 60.0;
                    if (mode.equals("transit")) durationMin += 5.0; // Wait time buffer
                    
                    act.setTravelDurationMin(Math.round(durationMin * 10.0) / 10.0);
                    
                    // Simple conflict check: if duration exceeds scheduled gap
                    // (For simplicity we assume time parsing is success)
                    if (durationMin > 30.0) {
                        warnings.add("Day " + act.getDayNumber() + ": Travel time between " + prev.getName() + " and " + act.getName() + " is high (" + act.getTravelDurationMin() + " mins). Consider transit adjustments.");
                    }
                }
            }
        }
    }

    private double haversine(double lat1, double lon1, double lat2, double lon2) {
        double R = 6371.0; // earth radius km
        double dLat = Math.toRadians(lat2 - lat1);
        double dLon = Math.toRadians(lon2 - lon1);
        double a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                   Math.cos(Math.toRadians(lat1)) * Math.cos(Math.toRadians(lat2)) *
                   Math.sin(dLon / 2) * Math.sin(dLon / 2);
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    }
}
