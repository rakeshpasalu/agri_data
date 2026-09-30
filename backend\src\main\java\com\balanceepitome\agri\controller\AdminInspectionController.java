package com.balanceepitome.agri.controller;

import com.balanceepitome.agri.service.CropSuitabilityEngine;
import com.balanceepitome.agri.service.CropSuitabilityRequest;
import com.balanceepitome.agri.service.CropSuitabilityResult;
import com.balanceepitome.agri.service.RegulatoryGate;
import com.balanceepitome.agri.service.RegulatoryDecision;
import org.springframework.web.bind.annotation.*;
import java.util.Map;
import java.util.List;
import java.util.UUID;
import java.time.LocalDate;

@RestController
@RequestMapping("/api/admin")
@CrossOrigin(origins = "*")
public class AdminInspectionController {

    private final CropSuitabilityEngine cropSuitabilityEngine;
    private final RegulatoryGate regulatoryGate;

    public AdminInspectionController(CropSuitabilityEngine cropSuitabilityEngine, RegulatoryGate regulatoryGate) {
        this.cropSuitabilityEngine = cropSuitabilityEngine;
        this.regulatoryGate = regulatoryGate;
    }

    @GetMapping("/status")
    public Map<String, Object> getSystemStatus() {
        return Map.of(
            "system", "Agricultural Intelligence Platform (Precision Farming)",
            "pilotGeography", "India -> Karnataka -> Chitradurga -> Molakalmuru -> Hosanagalapura",
            "evidenceEngine", "Deterministic / Rule-Based",
            "regulatoryBoundary", "CIB&RC Strict Enforcement Active",
            "version", "0.1.0-FOUNDATION"
        );
    }

    @GetMapping("/sources")
    public List<Map<String, Object>> getSources() {
        return List.of(
            Map.of("name", "UAS Bangalore Package of Practices", "authority", "UNIVERSITY", "geo", "Zone IV (Central Dry Zone)", "license", "YELLOW"),
            Map.of("name", "CIB&RC Major Uses & Banned List", "authority", "GOVERNMENT", "geo", "National (India)", "license", "GREEN"),
            Map.of("name", "KSSC Variety Catalogue", "authority", "STATE_ENTERPRISE", "geo", "Karnataka", "license", "GREEN"),
            Map.of("name", "ICAR-NBSS&LUP Soil Survey of Chitradurga", "authority", "RESEARCH_INSTITUTION", "geo", "District", "license", "YELLOW"),
            Map.of("name", "NASA POWER Agroclimatology", "authority", "GOVERNMENT (NASA)", "geo", "Point Reanalysis ~14.887, 76.842", "license", "GREEN"),
            Map.of("name", "Kumar Naik et al. 2020 (n=148 samples)", "authority", "PEER_REVIEWED_JOURNAL", "geo", "Molakalmuru Taluk", "license", "YELLOW")
        );
    }

    @GetMapping("/conflicts")
    public List<Map<String, Object>> getDocumentedConflicts() {
        return List.of(
            Map.of(
                "conflictId", "CONFLICT-002",
                "crop", "Groundnut",
                "parameter", "NPK Recommended Dose of Fertilizer (RDF)",
                "sourceA", "UASB PoP: 25:75:37.5 NPK kg/ha + 500kg gypsum",
                "sourceB", "NARP / CDZ Table: 25:50:25 NPK kg/ha (rainfed)",
                "cause", "Difference in irrigation assumption (irrigated vs rainfed) & soil calcium",
                "resolutionPolicy", "CONFLICTING_EVIDENCE preserved. Do not average. Require farm soil test + STCR calibration."
            )
        );
    }

    @PostMapping("/evaluate-suitability")
    public CropSuitabilityResult evaluateSuitability(@RequestBody CropSuitabilityRequest request) {
        return cropSuitabilityEngine.evaluate(request);
    }

    @GetMapping("/check-regulation")
    public RegulatoryDecision checkRegulation(
            @RequestParam String activeIngredient,
            @RequestParam String crop,
            @RequestParam String pest,
            @RequestParam(defaultValue = "Karnataka") String geography) {
        return regulatoryGate.check(activeIngredient, crop, pest, geography);
    }
}
