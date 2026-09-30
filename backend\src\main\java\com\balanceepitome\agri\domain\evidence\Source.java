package com.balanceepitome.agri.domain.evidence;

import com.balanceepitome.agri.domain.common.LicenseBand;
import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "source")
@Data
public class Source {
    @Id
    private UUID id;
    
    @Column(nullable = false)
    private String name;
    
    private String authorityLevel;
    private String url;
    private LocalDate publicationDate;
    private String geographicScope;
    
    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "license_band")
    private LicenseBand licenseBand;
    
    private ZonedDateTime retrievedAt;
    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
