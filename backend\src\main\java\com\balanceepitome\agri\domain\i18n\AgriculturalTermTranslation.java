package com.balanceepitome.agri.domain.i18n;

import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "agricultural_term_translation")
@Data
public class AgriculturalTermTranslation {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "term_id")
    private AgriculturalTerm term;

    private String languageCode;
    private String translatedTerm;
    private String script;
    private String romanized;
    private Boolean verified;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
