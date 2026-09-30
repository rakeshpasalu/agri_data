package com.balanceepitome.agri.domain.crop;

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
@Table(name = "crop_requirement")
@Data
public class CropRequirement {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_id")
    private Crop crop;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "variety_id")
    private CropVariety variety;

    private String parameter;
    private BigDecimal minValue;
    private BigDecimal maxValue;
    private String unit;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> condition;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "evidence_id")
    private Evidence evidence;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
