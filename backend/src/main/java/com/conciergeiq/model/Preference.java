package com.conciergeiq.model;

import jakarta.persistence.*;
import lombok.*;
import java.util.UUID;

@Entity
@Table(name = "preferences")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Preference {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @OneToOne
    @JoinColumn(name = "guest_id", nullable = false)
    private Guest guest;

    // Store as JSON string, e.g. "{\"adventure\":3,\"nature\":4}"
    @Column(name = "travel_style", columnDefinition = "TEXT")
    private String travelStyle;

    // Store as comma-separated string, e.g. "vegetarian,gluten-free"
    @Column(name = "dietary_restrictions", columnDefinition = "TEXT")
    private String dietaryRestrictions;

    // Store as comma-separated string, e.g. "wheelchair,minimal-walking"
    @Column(name = "accessibility_needs", columnDefinition = "TEXT")
    private String accessibilityNeeds;

    @Column(name = "budget_tier")
    private String budgetTier = "moderate";
}
