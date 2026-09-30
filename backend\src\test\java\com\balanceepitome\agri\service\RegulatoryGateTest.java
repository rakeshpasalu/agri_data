package com.balanceepitome.agri.service;

import com.balanceepitome.agri.service.impl.SimpleRegulatoryGate;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class RegulatoryGateTest {
    
    private final RegulatoryGate gate = new SimpleRegulatoryGate();
    
    @Test
    void whenApprovedChemical_thenApproved() {
        RegulatoryDecision decision = gate.check("azadirachtin", "Tomato", "Aphids", "Karnataka");
        assertEquals(DecisionStatus.APPROVED, decision.status());
    }
    
    @Test
    void whenBannedChemical_thenBanned() {
        RegulatoryDecision decision = gate.check("monocrotophos", "Cotton", "Bollworm", "Karnataka");
        assertEquals(DecisionStatus.BANNED, decision.status());
    }
    
    @Test
    void whenUnknownChemical_thenUnknown() {
        RegulatoryDecision decision = gate.check("unknown_chemical", "Rice", "Stem Borer", "Karnataka");
        assertEquals(DecisionStatus.UNKNOWN, decision.status());
    }
}
