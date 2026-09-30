package com.balanceepitome.agri.service.rag;

import java.util.List;

public interface RagService {
    List<EvidenceChunk> retrieveEvidence(RagSearchRequest request);
    void indexDocument(UUID sourceId, String content, RagMetadata metadata);
}
