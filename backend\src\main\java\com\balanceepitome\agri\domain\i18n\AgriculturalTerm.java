package com.balanceepitome.agri.domain.i18n;

import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "agricultural_term")
@Data
public class AgriculturalTerm {
    @Id
    private UUID id;

    @Column(nullable = false, unique = true)
    private String canonicalKey;

    private String category;
    private String englishTerm;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
