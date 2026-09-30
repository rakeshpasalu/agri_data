package com.balanceepitome.agri.domain.farm;

import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "agronomist_review")
@Data
public class AgronomistReview {
    @Id
    private UUID id;

    private UUID recommendationId;
    private String reviewerName;
    private String reviewerOrganization;
    private String reviewStatus; // APPROVED, REVISED, REJECTED
    
    @Column(columnDefinition = "TEXT")
    private String notes;

    private ZonedDateTime reviewedAt;
    private ZonedDateTime createdAt;
}
