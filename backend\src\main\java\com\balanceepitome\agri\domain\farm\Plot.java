package com.balanceepitome.agri.domain.farm;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Column;
import jakarta.persistence.Table;
import org.locationtech.jts.geom.Polygon;
import lombok.Data;
import java.util.UUID;
import java.math.BigDecimal;
import java.time.ZonedDateTime;

@Entity
@Table(name = "plot")
@Data
public class Plot {
    @Id
    private UUID id;
    
    @Column(name = "farm_id")
    private UUID farmId;
    
    private String name;
    
    @Column(columnDefinition = "geometry(Polygon, 4326)")
    private Polygon boundary;
    
    private BigDecimal areaHectares;
    private String soilType;
    private String irrigationType;
    private String waterSource;
    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
