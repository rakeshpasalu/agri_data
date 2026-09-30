package com.balanceepitome.agri.domain.seed;

import com.balanceepitome.agri.domain.crop.CropVariety;
import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "seed_product")
@Data
public class SeedProduct {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "variety_id")
    private CropVariety variety;

    private String brandName;
    private String certificationClass; // FOUNDATION, CERTIFIED, TRUTHFULLY_LABELED
    private BigDecimal packSizeKg;
    private BigDecimal mrpInr;
    private Boolean verifiedAvailable;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
