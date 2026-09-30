package com.balanceepitome.agri.service.rag;

import java.util.UUID;

public record EvidenceChunk(
    UUID chunkId,
    UUID sourceId,
    String sourceName,
    String documentTitle,
    String pageOrSection,
    String chunkText,
    RagMetadata metadata,
    double relevanceScore
) {}
