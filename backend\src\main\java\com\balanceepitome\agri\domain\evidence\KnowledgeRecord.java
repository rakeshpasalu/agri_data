package com.balanceepitome.agri.domain.evidence;

import com.balanceepitome.agri.domain.common.GeographicResolution;
import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.Map;
import java.util.UUID;

@Entity
@Table(name = "knowledge_record")
@Data
public class KnowledgeRecord {
    @Id
    private UUID id;

    private String category;
    private String subcategory;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> conditions;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> content;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "evidence_id")
    private Evidence evidence;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "geographic_resolution")
    private GeographicResolution geographicResolution;

    private LocalDate validFrom;
    private LocalDate validUntil;
    private UUID supersededBy;
    private String confidence;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
