package com.balanceepitome.agri.domain.farm;

import com.balanceepitome.agri.domain.common.DataProvenance;
import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "water_source")
@Data
public class WaterSource {
    @Id
    private UUID id;

    @Column(name = "farm_id")
    private UUID farmId;

    private String type;
    private BigDecimal depthMeters;
    private BigDecimal dischargeLpm;
    private String qualityClass;
    private LocalDate testedDate;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "data_provenance")
    private DataProvenance dataProvenance;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
