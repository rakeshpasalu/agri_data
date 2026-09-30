package com.balanceepitome.agri.domain.weather;

import jakarta.persistence.*;
import lombok.Data;
import org.locationtech.jts.geom.Point;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "weather_observation")
@Data
public class WeatherObservation {
    @Id
    private UUID id;

    @Column(columnDefinition = "geometry(Point, 4326)")
    private Point location;

    private LocalDate observationDate;
    private String observationType; // HISTORICAL_REANALYSIS, STATION_OBSERVED, MODEL_FORECAST
    private BigDecimal temperatureMaxC;
    private BigDecimal temperatureMinC;
    private BigDecimal temperatureMeanC;
    private BigDecimal rainfallMm;
    private BigDecimal humidityPct;
    private BigDecimal windSpeedMs;
    private BigDecimal solarRadiationMjm2;
    private BigDecimal et0Mm;
    private String provider;

    private ZonedDateTime retrievedAt;
    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
