package com.balanceepitome.agri.domain.weather;

import lombok.Builder;
import lombok.Data;
import java.math.BigDecimal;
import java.util.Map;

@Data
@Builder
public class WeatherClimatology {
    private String locationDescription;
    private BigDecimal elevationMeters;
    private BigDecimal annualMeanTempC;
    private BigDecimal annualPrecipitationMm;
    private Map<Integer, BigDecimal> monthlyPrecipitationMm;
    private Map<Integer, BigDecimal> monthlyMeanTempC;
    private String provider;
    private String baselinePeriod; // e.g., 2001-2020
}
