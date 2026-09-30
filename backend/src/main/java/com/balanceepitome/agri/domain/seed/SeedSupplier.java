package com.balanceepitome.agri.domain.seed;

import jakarta.persistence.*;
import lombok.Data;
import org.locationtech.jts.geom.Point;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "seed_supplier")
@Data
public class SeedSupplier {
    @Id
    private UUID id;

    private String name;
    private String supplierType; // KSSC_OUTLET, RSK, COOPERATIVE, PRIVATE_DEALER
    private String contactNumber;
    private String address;
    private String taluk;
    private String district;

    @Column(columnDefinition = "geometry(Point, 4326)")
    private Point location;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
