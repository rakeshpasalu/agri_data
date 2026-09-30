package com.balanceepitome.agri.service.rag;

import java.time.LocalDate;
import java.util.List;

public record RagMetadata(
    String country,
    String region,
    String agroClimaticZone,
    String crop,
    String season,
    String topic,
    String authority,
    LocalDate publicationDate,
    LocalDate validUntil,
    String licenseBand,
    String language,
    List<String> keywords
) {}
