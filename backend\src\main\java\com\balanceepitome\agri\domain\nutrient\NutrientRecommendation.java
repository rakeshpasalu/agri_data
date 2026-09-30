package com.balanceepitome.agri.domain.nutrient;

import com.balanceepitome.agri.domain.crop.Crop;
import com.balanceepitome.agri.domain.crop.CropVariety;
import com.balanceepitome.agri.domain.evidence.Evidence;
import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
import java.math.BigDecimal;
import java.time.ZonedDateTime;
import java.util.Map;
import java.util.UUID;

@Entity
@Table(name = "nutrient_recommendation")
@Data
public class NutrientRecommendation {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_id")
    private Crop crop;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "variety_id")
    private CropVariety variety;

    private String soilType;
    private String irrigationStatus;
    private String zone;

    private BigDecimal nKgha;
    private BigDecimal p2o5Kgha;
    private BigDecimal k2oKgha;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> otherInputs;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "evidence_id")
    private Evidence evidence;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> conditions;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
