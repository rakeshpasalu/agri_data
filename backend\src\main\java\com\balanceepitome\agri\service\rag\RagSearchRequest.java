package com.balanceepitome.agri.service.rag;

public record RagSearchRequest(
    String query,
    String targetCrop,
    String targetZone,
    String targetSeason,
    String targetLanguage,
    int maxResults,
    boolean strictZoneFilter
) {}
