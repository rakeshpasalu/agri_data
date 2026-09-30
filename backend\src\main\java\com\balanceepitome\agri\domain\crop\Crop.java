package com.balanceepitome.agri.domain.crop;

import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "crop")
@Data
public class Crop {
    @Id
    private UUID id;

    @Column(nullable = false)
    private String canonicalName;

    private String scientificName;
    private String cropType;
    private String cropGroup;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
