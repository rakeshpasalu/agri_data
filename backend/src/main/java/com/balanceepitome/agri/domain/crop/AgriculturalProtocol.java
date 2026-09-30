package com.balanceepitome.agri.domain.crop;

import com.balanceepitome.agri.domain.evidence.Evidence;
import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
import java.time.ZonedDateTime;
import java.util.Map;
import java.util.UUID;

@Entity
@Table(name = "agricultural_protocol")
@Data
public class AgriculturalProtocol {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_id")
    private Crop crop;

    private String stageName;
    private Integer daysAfterSowingMin;
    private Integer daysAfterSowingMax;
    
    @Column(columnDefinition = "TEXT")
    private String protocolDescription;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> inputDetails;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "evidence_id")
    private Evidence evidence;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
