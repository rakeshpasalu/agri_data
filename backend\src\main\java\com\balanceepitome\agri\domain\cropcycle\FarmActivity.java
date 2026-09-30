package com.balanceepitome.agri.domain.cropcycle;

import com.balanceepitome.agri.domain.common.DataProvenance;
import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "farm_activity")
@Data
public class FarmActivity {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_cycle_id")
    private CropCycle cropCycle;

    private String activityType;
    private LocalDate activityDate;
    
    @Column(columnDefinition = "TEXT")
    private String description;
    
    private String inputProduct;
    private BigDecimal quantity;
    private String unit;
    private BigDecimal costInr;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "data_provenance")
    private DataProvenance dataProvenance;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
