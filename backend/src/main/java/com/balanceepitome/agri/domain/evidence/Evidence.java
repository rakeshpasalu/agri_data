package com.balanceepitome.agri.domain.evidence;

import com.balanceepitome.agri.domain.common.ObservationType;
import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
import java.time.ZonedDateTime;
import java.util.Map;
import java.util.UUID;

@Entity
@Table(name = "evidence")
@Data
public class Evidence {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "source_id")
    private Source source;

    private String documentUrl;
    private String documentHash;
    private String pageReference;

    @Column(columnDefinition = "TEXT")
    private String claimText;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> geographicApplicability;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "observation_type")
    private ObservationType observationType;

    private Boolean verified;
    private ZonedDateTime verificationDate;

    @Column(columnDefinition = "TEXT")
    private String notes;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
