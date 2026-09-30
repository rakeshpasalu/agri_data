package com.balanceepitome.agri.domain.farm;

import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "farmer_feedback")
@Data
public class FarmerFeedback {
    @Id
    private UUID id;

    @Column(name = "farmer_id")
    private UUID farmerId;

    private UUID recommendationId;
    private Integer rating;
    
    @Column(columnDefinition = "TEXT")
    private String comment;
    
    private Boolean adopted;
    private ZonedDateTime createdAt;
}
