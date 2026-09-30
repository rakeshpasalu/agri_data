package com.balanceepitome.agri.service;

import org.locationtech.jts.geom.Point;
import java.time.LocalDate;
import java.util.List;

public interface WeatherProvider {
    List<Object> getHistorical(Point location, LocalDate from, LocalDate to);
    List<Object> getForecast(Point location, int days);
    Object getClimatology(Point location);
    String getProviderName();
}
