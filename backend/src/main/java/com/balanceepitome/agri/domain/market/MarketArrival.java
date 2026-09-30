package com.balanceepitome.agri.domain.market;

import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "market_arrival")
@Data
public class MarketArrival {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "market_id")
    private Market market;

    private String commodity;
    private LocalDate arrivalDate;
    private BigDecimal quantityTonnes;
    private String unitOfMeasure;

    private ZonedDateTime createdAt;
}
