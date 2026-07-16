package com.conciergeiq.service;

import org.springframework.stereotype.Service;
import java.util.*;

@Service
public class VectorSearchService {

    // Preloaded local travel guide and event reviews
    private static final List<Map<String, String>> EVENTS_KNOWLEDGE_BASE = Arrays.asList(
        // Paris
        createEventDoc("paris", "attraction", "Eiffel Tower Light Show", "Highly-rated nightly light show at the Eiffel Tower. Starts every hour on the hour after sunset. Address: Champ de Mars, Phone: +33 892 70 12 39."),
        createEventDoc("paris", "museum", "Louvre Guided Art Tour", "Skip-the-line group tour of the Louvre Museum featuring the Mona Lisa. Hours: 09:00 - 18:00. Cost: $45. Phone: +33 1 40 20 53 17."),
        createEventDoc("paris", "emergency", "American Hospital of Paris", "Popular English-speaking emergency hospital in Neuilly-sur-Seine. Phone: +33 1 46 41 25 25."),
        createEventDoc("paris", "event", "Seine River Dinner Cruise", "Romantic 2-hour dinner cruise on the Seine River. Highly rated reviews. Cost: $85. Phone: +33 1 44 68 06 30."),
        // Tokyo
        createEventDoc("tokyo", "attraction", "Sensoji Temple Light Show", "Historic Asakusa temple beautifully lit up after dark. Open 24 hours. Free entry. Phone: +81 3-3842-0181."),
        createEventDoc("tokyo", "museum", "teamLab Planets Toyosu", "Immersive digital projection museum where you walk through water. Highly rated reviews. Hours: 09:00 - 22:00. Cost: $28."),
        createEventDoc("tokyo", "emergency", "St. Luke's International Hospital", "English-speaking emergency hospital in Chuo City, Tokyo. Phone: +81 3-3541-5151."),
        createEventDoc("tokyo", "event", "Shibuya Crossing Walking Tour", "Guided night tour of Shibuya neon signs and local ramen spots. Cost: $20.")
    );

    private static Map<String, String> createEventDoc(String city, String category, String name, String details) {
        Map<String, String> doc = new HashMap<>();
        doc.put("city", city);
        doc.put("category", category);
        doc.put("name", name);
        doc.put("details", details);
        return doc;
    }

    /**
     * Simulates Amazon OpenSearch vector search.
     * Uses keyword overlap scoring.
     */
    public List<Map<String, String>> search(String query, String city) {
        String cleanQuery = query.toLowerCase();
        String cleanCity = city != null ? city.toLowerCase().trim() : null;
        
        List<Map<String, Object>> scoredDocs = new ArrayList<>();
        
        for (Map<String, String> doc : EVENTS_KNOWLEDGE_BASE) {
            // City filter
            if (cleanCity != null && !doc.get("city").equals(cleanCity)) {
                continue;
            }
            
            double score = 0.0;
            String textToSearch = (doc.get("name") + " " + doc.get("details") + " " + doc.get("category")).toLowerCase();
            
            String[] queryWords = cleanQuery.split("\\s+");
            for (String qw : queryWords) {
                if (qw.length() > 3 && textToSearch.contains(qw)) {
                    score += 1.0;
                }
            }
            
            // Category match boost
            if (cleanQuery.contains(doc.get("category"))) {
                score += 2.0;
            }
            
            if (score > 0.0) {
                Map<String, Object> scored = new HashMap<>(doc);
                scored.put("score", score);
                scoredDocs.add(scored);
            }
        }
        
        // Sort by score desc
        scoredDocs.sort((a, b) -> Double.compare((Double) b.get("score"), (Double) a.get("score")));
        
        List<Map<String, String>> results = new ArrayList<>();
        for (int i = 0; i < Math.min(scoredDocs.size(), 3); i++) {
            Map<String, Object> scored = scoredDocs.get(i);
            Map<String, String> docResult = new HashMap<>();
            docResult.put("city", (String) scored.get("city"));
            docResult.put("category", (String) scored.get("category"));
            docResult.put("name", (String) scored.get("name"));
            docResult.put("details", (String) scored.get("details"));
            results.add(docResult);
        }
        
        return results;
    }
}
