package com.balanceepitome.agri.domain.crop;

import com.balanceepitome.agri.domain.evidence.Evidence;
import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "crop_calendar")
@Data
public class CropCalendar {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_id")
    private Crop crop;

    private String zone;
    private String season;
    private Integer sowingStartMonth;
    private Integer sowingEndMonth;
    private Integer harvestStartMonth;
    private Integer harvestEndMonth;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "evidence_id")
    private Evidence evidence;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
