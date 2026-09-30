package com.balanceepitome.agri.domain.crop;

import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "crop_name_mapping")
@Data
public class CropNameMapping {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_id")
    private Crop crop;

    private String languageCode;
    private String name;
    private String script;
    private Boolean isPrimary;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
