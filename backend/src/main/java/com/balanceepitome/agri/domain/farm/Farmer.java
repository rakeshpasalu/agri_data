package com.balanceepitome.agri.domain.farm;

import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "farmer")
@Data
public class Farmer {
    @Id
    private UUID id;

    @Column(nullable = false)
    private String name;

    private String phoneHash;
    private String preferredLanguage;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
