package com.balanceepitome.agri.domain.pest;

import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "disease")
@Data
public class Disease {
    @Id
    private UUID id;

    @Column(nullable = false)
    private String canonicalName;

    private String scientificName;
    private String causalAgent;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
