package com.balanceepitome.agri.domain.market;

import com.balanceepitome.agri.domain.evidence.Source;
import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "market_price")
@Data
public class MarketPrice {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "market_id")
    private Market market;

    private String commodity;
    private String variety;
    private String grade;
    private BigDecimal arrivalQuantity;
    private BigDecimal minPricePerQuintal;
    private BigDecimal maxPricePerQuintal;
    private BigDecimal modalPricePerQuintal;
    private LocalDate priceDate;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "source_id")
    private Source source;

    private ZonedDateTime retrievedAt;
    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
