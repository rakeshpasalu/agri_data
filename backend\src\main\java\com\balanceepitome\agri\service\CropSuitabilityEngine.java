package com.balanceepitome.agri.service;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

public interface CropSuitabilityEngine {
    CropSuitabilityResult evaluate(CropSuitabilityRequest request);
}

record EvidenceReference(UUID evidenceId, String source) {}

enum SuitabilityStatus {
    SUITABLE, CONDITIONALLY_SUITABLE, UNSUITABLE, INSUFFICIENT_DATA
}

record SuitabilityReason(String reasonType, String description) {}

record CropSuitabilityRequest(
    UUID farmId, 
    UUID plotId, 
    String cropCanonicalName,
    LocalDate plantingDate, 
    String season
) {}

record CropSuitabilityResult(
    String cropName, 
    SuitabilityStatus status,
    List<SuitabilityReason> reasons,
    List<String> missingInformation,
    List<EvidenceReference> evidence
) {}
