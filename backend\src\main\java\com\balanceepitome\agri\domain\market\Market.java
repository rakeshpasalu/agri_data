package com.balanceepitome.agri.domain.market;

import jakarta.persistence.*;
import lombok.Data;
import org.locationtech.jts.geom.Point;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "market")
@Data
public class Market {
    @Id
    private UUID id;

    @Column(nullable = false)
    private String name;

    private String marketType;

    @Column(columnDefinition = "geometry(Point, 4326)")
    private Point location;

    private String district;
    private String state;
    private String agmarknetCode;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
