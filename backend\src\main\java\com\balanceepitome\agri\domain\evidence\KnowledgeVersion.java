package com.balanceepitome.agri.domain.evidence;

import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
import java.time.ZonedDateTime;
import java.util.Map;
import java.util.UUID;

@Entity
@Table(name = "knowledge_version")
@Data
public class KnowledgeVersion {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "knowledge_record_id")
    private KnowledgeRecord knowledgeRecord;

    private Integer versionNumber;
    private String changedBy;
    private ZonedDateTime changedAt;
    
    @Column(columnDefinition = "TEXT")
    private String changeReason;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> previousContent;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
