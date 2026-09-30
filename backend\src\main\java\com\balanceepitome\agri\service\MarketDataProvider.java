package com.balanceepitome.agri.service;

import java.time.LocalDate;
import java.util.List;

public interface MarketDataProvider {
    List<Object> getLatestPrices(String commodity, String state, String district);
    List<Object> getHistoricalPrices(String commodity, String market, LocalDate from, LocalDate to);
    String getProviderName();
}
