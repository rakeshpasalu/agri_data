package com.balanceepitome.agri.domain.cropcycle;

import com.balanceepitome.agri.domain.common.DataProvenance;
import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "sale")
@Data
public class Sale {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "harvest_id")
    private Harvest harvest;

    private LocalDate saleDate;
    private String marketName;
    private String buyerType;
    private BigDecimal pricePerKgInr;
    private BigDecimal quantityKg;
    private BigDecimal transportCostInr;
    private BigDecimal commissionInr;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "data_provenance")
    private DataProvenance dataProvenance;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
