package com.balanceepitome.agri.domain.cropcycle;

import com.balanceepitome.agri.domain.common.CropCycleStatus;
import com.balanceepitome.agri.domain.crop.Crop;
import com.balanceepitome.agri.domain.crop.CropVariety;
import com.balanceepitome.agri.domain.farm.Plot;
import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "crop_cycle")
@Data
public class CropCycle {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "plot_id")
    private Plot plot;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_id")
    private Crop crop;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "variety_id")
    private CropVariety variety;

    private String season;
    private LocalDate sowingDate;
    private LocalDate expectedHarvestDate;
    private LocalDate actualHarvestDate;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "crop_cycle_status")
    private CropCycleStatus status;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
