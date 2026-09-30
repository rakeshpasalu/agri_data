package com.balanceepitome.agri.domain.pest;

import com.balanceepitome.agri.domain.common.ManagementType;
import com.balanceepitome.agri.domain.crop.Crop;
import com.balanceepitome.agri.domain.evidence.Evidence;
import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "disease_management")
@Data
public class DiseaseManagement {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "disease_id")
    private Disease disease;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_id")
    private Crop crop;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "management_type")
    private ManagementType managementType;

    @Column(columnDefinition = "TEXT")
    private String description;

    private String activeIngredient;
    private String formulation;
    private BigDecimal dose;
    private String doseUnit;
    private Integer phiDays;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "evidence_id")
    private Evidence evidence;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
