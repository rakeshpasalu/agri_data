package com.balanceepitome.agri.service.impl;

import com.balanceepitome.agri.service.*;
import org.springframework.stereotype.Service;

@Service
public class SimpleRegulatoryGate implements RegulatoryGate {
    @Override
    public RegulatoryDecision check(String activeIngredient, String crop, String pest, String geography) {
        if ("monocrotophos".equalsIgnoreCase(activeIngredient)) {
            return new RegulatoryDecision(DecisionStatus.BANNED, "Banned by CIBRC.");
        }
        if ("azadirachtin".equalsIgnoreCase(activeIngredient)) {
            return new RegulatoryDecision(DecisionStatus.APPROVED, "Approved biopesticide.");
        }
        return new RegulatoryDecision(DecisionStatus.UNKNOWN, "Chemical not found in regulatory database.");
    }
}
