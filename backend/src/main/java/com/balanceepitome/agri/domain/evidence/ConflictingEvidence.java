package com.balanceepitome.agri.domain.evidence;

import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
import java.time.ZonedDateTime;
import java.util.Map;
import java.util.UUID;

@Entity
@Table(name = "conflicting_evidence")
@Data
public class ConflictingEvidence {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "knowledge_record_a_id")
    private KnowledgeRecord knowledgeRecordA;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "knowledge_record_b_id")
    private KnowledgeRecord knowledgeRecordB;

    private String conflictType;
    private String resolutionStatus;
    
    @Column(columnDefinition = "TEXT")
    private String resolutionNotes;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> conditionsDiffer;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
