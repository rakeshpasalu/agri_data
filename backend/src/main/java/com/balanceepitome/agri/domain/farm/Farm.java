package com.balanceepitome.agri.domain.farm;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Column;
import jakarta.persistence.Table;
import org.locationtech.jts.geom.Point;
import org.locationtech.jts.geom.Polygon;
import lombok.Data;
import java.util.UUID;
import java.math.BigDecimal;
import java.time.ZonedDateTime;

@Entity
@Table(name = "farm")
@Data
public class Farm {
    @Id
    private UUID id;
    
    @Column(name = "farmer_id")
    private UUID farmerId;
    
    private String name;
    
    @Column(columnDefinition = "geometry(Point, 4326)")
    private Point location;
    
    @Column(columnDefinition = "geometry(Polygon, 4326)")
    private Polygon boundary;
    
    private BigDecimal areaHectares;
    private String surveyNumber;
    private String villageCode;
    private String taluk;
    private String district;
    private String state;
    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
