package com.balanceepitome.agri.domain.cropcycle;

import com.balanceepitome.agri.domain.common.DataProvenance;
import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "harvest")
@Data
public class Harvest {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_cycle_id")
    private CropCycle cropCycle;

    private LocalDate harvestDate;
    private BigDecimal quantityKg;
    private String qualityGrade;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "data_provenance")
    private DataProvenance dataProvenance;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
