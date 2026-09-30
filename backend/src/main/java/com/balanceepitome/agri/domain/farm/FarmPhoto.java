package com.balanceepitome.agri.domain.farm;

import com.balanceepitome.agri.domain.common.DataProvenance;
import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "farm_photo")
@Data
public class FarmPhoto {
    @Id
    private UUID id;

    @Column(name = "plot_id")
    private UUID plotId;

    private String photoUrl;
    private String caption;
    private String tags;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "data_provenance")
    private DataProvenance dataProvenance;

    private ZonedDateTime capturedAt;
    private ZonedDateTime createdAt;
}
