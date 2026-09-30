package com.balanceepitome.agri.domain.regulation;

import com.balanceepitome.agri.domain.common.RegulatoryStatus;
import com.balanceepitome.agri.domain.evidence.Source;
import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "input_regulation")
@Data
public class InputRegulation {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "input_product_id")
    private InputProduct inputProduct;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "regulatory_status")
    private RegulatoryStatus regulatoryStatus;

    private LocalDate effectiveDate;
    private LocalDate expiryDate;
    
    @Column(columnDefinition = "TEXT[]")
    private String[] applicableCrops;

    @Column(columnDefinition = "TEXT[]")
    private String[] applicablePests;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "source_id")
    private Source source;

    @Column(columnDefinition = "TEXT")
    private String notes;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
