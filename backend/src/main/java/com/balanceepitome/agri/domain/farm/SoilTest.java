package com.balanceepitome.agri.domain.farm;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Column;
import jakarta.persistence.Table;
import jakarta.persistence.Enumerated;
import jakarta.persistence.EnumType;
import lombok.Data;
import java.util.UUID;
import java.math.BigDecimal;
import java.time.LocalDate;
import com.balanceepitome.agri.domain.common.DataProvenance;

@Entity
@Table(name = "soil_test")
@Data
public class SoilTest {
    @Id
    private UUID id;
    
    @Column(name = "plot_id")
    private UUID plotId;
    
    private LocalDate testDate;
    private BigDecimal ph;
    private BigDecimal ecDsm;
    private BigDecimal organicCarbonPct;
    private BigDecimal nitrogenKgha;
    private BigDecimal phosphorusKgha;
    private BigDecimal potassiumKgha;
    
    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "data_provenance")
    private DataProvenance dataProvenance;
}
