package com.balanceepitome.agri.service;

public interface RegulatoryGate {
    RegulatoryDecision check(String activeIngredient, String crop, String pest, String geography);
}

enum DecisionStatus {
    APPROVED, BANNED, UNKNOWN
}

record RegulatoryDecision(DecisionStatus status, String notes) {}
