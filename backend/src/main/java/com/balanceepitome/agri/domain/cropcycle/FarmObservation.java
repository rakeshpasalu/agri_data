package com.balanceepitome.agri.domain.cropcycle;

import com.balanceepitome.agri.domain.common.DataProvenance;
import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "farm_observation")
@Data
public class FarmObservation {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_cycle_id")
    private CropCycle cropCycle;

    private LocalDate observationDate;
    private String category;
    
    @Column(columnDefinition = "TEXT")
    private String description;
    
    private String severity;
    private String photoUrl;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "data_provenance")
    private DataProvenance dataProvenance;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
