package com.balanceepitome.agri.domain.pest;

import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "pest")
@Data
public class Pest {
    @Id
    private UUID id;

    @Column(nullable = false)
    private String canonicalName;

    private String scientificName;
    private String pestType;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
