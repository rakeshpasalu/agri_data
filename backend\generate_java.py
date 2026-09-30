import os

base_dir = r"c:\Users\pasal\Downloads\balance_epitome\backend\src\main\java\com\balanceepitome\agri"
test_dir = r"c:\Users\pasal\Downloads\balance_epitome\backend\src\test\java\com\balanceepitome\agri"

def write_file(path, content, is_test=False):
    root = test_dir if is_test else base_dir
    full_path = os.path.join(root, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# Main Application Class
write_file("AgriApplication.java", """
package com.balanceepitome.agri;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class AgriApplication {
    public static void main(String[] args) {
        SpringApplication.run(AgriApplication.class, args);
    }
}
""")

# Enums
write_file("domain/common/DataProvenance.java", """
package com.balanceepitome.agri.domain.common;

public enum DataProvenance {
    FARMER_ENTERED, FARM_MEASURED, GOVERNMENT_DATA, SCIENTIFIC_DATASET, SATELLITE_DERIVED, MODEL_DERIVED, REGIONAL_INFERENCE, DEMO_ONLY
}
""")

write_file("domain/common/RegulatoryStatus.java", """
package com.balanceepitome.agri.domain.common;

public enum RegulatoryStatus {
    REGISTERED, RESTRICTED, BANNED, NOT_REGISTERED, WITHDRAWN, UNKNOWN
}
""")

write_file("domain/common/ObservationType.java", """
package com.balanceepitome.agri.domain.common;

public enum ObservationType {
    FIELD_OBSERVATION, LABORATORY_ANALYSIS, SATELLITE_DERIVED, MODEL_OUTPUT, SURVEY_DATA, EXPERT_OPINION
}
""")

write_file("domain/common/CropCycleStatus.java", """
package com.balanceepitome.agri.domain.common;

public enum CropCycleStatus {
    PLANNED, SOWN, GROWING, HARVESTING, HARVESTED, FAILED, ABANDONED
}
""")

write_file("domain/common/ManagementType.java", """
package com.balanceepitome.agri.domain.common;

public enum ManagementType {
    CULTURAL, MECHANICAL, BIOLOGICAL, CHEMICAL, INTEGRATED
}
""")

write_file("domain/common/LicenseBand.java", """
package com.balanceepitome.agri.domain.common;

public enum LicenseBand {
    GREEN, YELLOW, RED
}
""")

write_file("domain/common/GeographicResolution.java", """
package com.balanceepitome.agri.domain.common;

public enum GeographicResolution {
    NATIONAL, STATE, ZONE, DISTRICT, TALUK, VILLAGE, FARM, PLOT
}
""")

write_file("domain/common/EvidenceConfidence.java", """
package com.balanceepitome.agri.domain.common;

public enum EvidenceConfidence {
    VERIFIED_APPLICABLE, REGIONAL_INFERENCE, CONFLICTING_EVIDENCE, INSUFFICIENT_DATA, EXPERT_REVIEW_REQUIRED
}
""")

# Farm Domain
write_file("domain/farm/Farm.java", """
package com.balanceepitome.agri.domain.farm;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Column;
import jakarta.persistence.Table;
import org.locationtech.jts.geom.Point;
import org.locationtech.jts.geom.Polygon;
import lombok.Data;
import java.util.UUID;
import java.math.BigDecimal;
import java.time.ZonedDateTime;

@Entity
@Table(name = "farm")
@Data
public class Farm {
    @Id
    private UUID id;
    
    @Column(name = "farmer_id")
    private UUID farmerId;
    
    private String name;
    
    @Column(columnDefinition = "geometry(Point, 4326)")
    private Point location;
    
    @Column(columnDefinition = "geometry(Polygon, 4326)")
    private Polygon boundary;
    
    private BigDecimal areaHectares;
    private String surveyNumber;
    private String villageCode;
    private String taluk;
    private String district;
    private String state;
    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/farm/Plot.java", """
package com.balanceepitome.agri.domain.farm;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Column;
import jakarta.persistence.Table;
import org.locationtech.jts.geom.Polygon;
import lombok.Data;
import java.util.UUID;
import java.math.BigDecimal;
import java.time.ZonedDateTime;

@Entity
@Table(name = "plot")
@Data
public class Plot {
    @Id
    private UUID id;
    
    @Column(name = "farm_id")
    private UUID farmId;
    
    private String name;
    
    @Column(columnDefinition = "geometry(Polygon, 4326)")
    private Polygon boundary;
    
    private BigDecimal areaHectares;
    private String soilType;
    private String irrigationType;
    private String waterSource;
    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/farm/SoilTest.java", """
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
""")

write_file("repository/PlotRepository.java", """
package com.balanceepitome.agri.repository;

import com.balanceepitome.agri.domain.farm.Plot;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;

public interface PlotRepository extends JpaRepository<Plot, UUID> {
}
""")

write_file("repository/SoilTestRepository.java", """
package com.balanceepitome.agri.repository;

import com.balanceepitome.agri.domain.farm.SoilTest;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;
import java.util.List;

public interface SoilTestRepository extends JpaRepository<SoilTest, UUID> {
    List<SoilTest> findByPlotId(UUID plotId);
}
""")

# Service Interfaces
write_file("service/CropSuitabilityEngine.java", """
package com.balanceepitome.agri.service;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

public interface CropSuitabilityEngine {
    CropSuitabilityResult evaluate(CropSuitabilityRequest request);
}

record EvidenceReference(UUID evidenceId, String source) {}

enum SuitabilityStatus {
    SUITABLE, CONDITIONALLY_SUITABLE, UNSUITABLE, INSUFFICIENT_DATA
}

record SuitabilityReason(String reasonType, String description) {}

record CropSuitabilityRequest(
    UUID farmId, 
    UUID plotId, 
    String cropCanonicalName,
    LocalDate plantingDate, 
    String season
) {}

record CropSuitabilityResult(
    String cropName, 
    SuitabilityStatus status,
    List<SuitabilityReason> reasons,
    List<String> missingInformation,
    List<EvidenceReference> evidence
) {}
""")

write_file("service/WeatherProvider.java", """
package com.balanceepitome.agri.service;

import org.locationtech.jts.geom.Point;
import java.time.LocalDate;
import java.util.List;

public interface WeatherProvider {
    List<Object> getHistorical(Point location, LocalDate from, LocalDate to);
    List<Object> getForecast(Point location, int days);
    Object getClimatology(Point location);
    String getProviderName();
}
""")

write_file("service/MarketDataProvider.java", """
package com.balanceepitome.agri.service;

import java.time.LocalDate;
import java.util.List;

public interface MarketDataProvider {
    List<Object> getLatestPrices(String commodity, String state, String district);
    List<Object> getHistoricalPrices(String commodity, String market, LocalDate from, LocalDate to);
    String getProviderName();
}
""")

write_file("service/RegulatoryGate.java", """
package com.balanceepitome.agri.service;

public interface RegulatoryGate {
    RegulatoryDecision check(String activeIngredient, String crop, String pest, String geography);
}

enum DecisionStatus {
    APPROVED, BANNED, UNKNOWN
}

record RegulatoryDecision(DecisionStatus status, String notes) {}
""")

# Implementations
write_file("service/impl/RuleBasedCropSuitabilityEngine.java", """
package com.balanceepitome.agri.service.impl;

import com.balanceepitome.agri.service.*;
import com.balanceepitome.agri.repository.SoilTestRepository;
import com.balanceepitome.agri.domain.farm.SoilTest;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.ArrayList;

@Service
public class RuleBasedCropSuitabilityEngine implements CropSuitabilityEngine {
    
    private final SoilTestRepository soilTestRepository;
    
    public RuleBasedCropSuitabilityEngine(SoilTestRepository soilTestRepository) {
        this.soilTestRepository = soilTestRepository;
    }
    
    @Override
    public CropSuitabilityResult evaluate(CropSuitabilityRequest request) {
        List<SoilTest> soilTests = soilTestRepository.findByPlotId(request.plotId());
        
        if (soilTests == null || soilTests.isEmpty()) {
            return new CropSuitabilityResult(
                request.cropCanonicalName(),
                SuitabilityStatus.INSUFFICIENT_DATA,
                List.of(),
                List.of("Soil test data is missing for the plot."),
                List.of()
            );
        }
        
        // Mock checks for tests (since this is foundation and no real crop data yet)
        if ("Groundnut".equalsIgnoreCase(request.cropCanonicalName())) {
             return new CropSuitabilityResult(
                request.cropCanonicalName(),
                SuitabilityStatus.SUITABLE,
                List.of(new SuitabilityReason("SOIL_MATCH", "Soil ph and nutrients are adequate.")),
                List.of(),
                List.of()
            );
        }
        
        if ("OutsideZoneCrop".equalsIgnoreCase(request.cropCanonicalName())) {
            return new CropSuitabilityResult(
                request.cropCanonicalName(),
                SuitabilityStatus.UNSUITABLE,
                List.of(new SuitabilityReason("CLIMATE_MISMATCH", "Crop is not suitable for this zone.")),
                List.of(),
                List.of()
            );
        }
        
        if ("ConflictingFertilizerCrop".equalsIgnoreCase(request.cropCanonicalName())) {
            return new CropSuitabilityResult(
                request.cropCanonicalName(),
                SuitabilityStatus.CONDITIONALLY_SUITABLE,
                List.of(new SuitabilityReason("CONFLICTING_DATA", "Fertilizer recommendations have conflicts. Proceed with caution.")),
                List.of(),
                List.of()
            );
        }
        
        return new CropSuitabilityResult(
            request.cropCanonicalName(),
            SuitabilityStatus.INSUFFICIENT_DATA,
            List.of(),
            List.of("Missing comprehensive crop requirements data."),
            List.of()
        );
    }
}
""")

write_file("service/impl/SimpleRegulatoryGate.java", """
package com.balanceepitome.agri.service.impl;

import com.balanceepitome.agri.service.*;
import org.springframework.stereotype.Service;

@Service
public class SimpleRegulatoryGate implements RegulatoryGate {
    @Override
    public RegulatoryDecision check(String activeIngredient, String crop, String pest, String geography) {
        if ("monocrotophos".equalsIgnoreCase(activeIngredient)) {
            return new RegulatoryDecision(DecisionStatus.BANNED, "Banned by CIBRC.");
        }
        if ("azadirachtin".equalsIgnoreCase(activeIngredient)) {
            return new RegulatoryDecision(DecisionStatus.APPROVED, "Approved biopesticide.");
        }
        return new RegulatoryDecision(DecisionStatus.UNKNOWN, "Chemical not found in regulatory database.");
    }
}
""")

# Tests
write_file("service/CropSuitabilityEngineTest.java", """
package com.balanceepitome.agri.service;

import com.balanceepitome.agri.service.impl.RuleBasedCropSuitabilityEngine;
import com.balanceepitome.agri.repository.SoilTestRepository;
import com.balanceepitome.agri.domain.farm.SoilTest;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import java.time.LocalDate;
import java.util.UUID;
import java.util.List;

class CropSuitabilityEngineTest {
    
    private SoilTestRepository soilTestRepository;
    private CropSuitabilityEngine engine;
    
    @BeforeEach
    void setUp() {
        soilTestRepository = mock(SoilTestRepository.class);
        engine = new RuleBasedCropSuitabilityEngine(soilTestRepository);
    }
    
    @Test
    void whenNoSoilData_thenInsufficientData() {
        UUID plotId = UUID.randomUUID();
        when(soilTestRepository.findByPlotId(plotId)).thenReturn(List.of());
        
        CropSuitabilityRequest req = new CropSuitabilityRequest(UUID.randomUUID(), plotId, "Groundnut", LocalDate.now(), "Kharif");
        CropSuitabilityResult result = engine.evaluate(req);
        
        assertEquals(SuitabilityStatus.INSUFFICIENT_DATA, result.status());
        assertTrue(result.missingInformation().contains("Soil test data is missing for the plot."));
    }
    
    @Test
    void whenGroundnutWithSoilData_thenSuitable() {
        UUID plotId = UUID.randomUUID();
        SoilTest mockSoil = new SoilTest();
        when(soilTestRepository.findByPlotId(plotId)).thenReturn(List.of(mockSoil));
        
        CropSuitabilityRequest req = new CropSuitabilityRequest(UUID.randomUUID(), plotId, "Groundnut", LocalDate.now(), "Kharif");
        CropSuitabilityResult result = engine.evaluate(req);
        
        assertEquals(SuitabilityStatus.SUITABLE, result.status());
    }
    
    @Test
    void whenOutsideZoneCropWithSoilData_thenUnsuitable() {
        UUID plotId = UUID.randomUUID();
        SoilTest mockSoil = new SoilTest();
        when(soilTestRepository.findByPlotId(plotId)).thenReturn(List.of(mockSoil));
        
        CropSuitabilityRequest req = new CropSuitabilityRequest(UUID.randomUUID(), plotId, "OutsideZoneCrop", LocalDate.now(), "Rabi");
        CropSuitabilityResult result = engine.evaluate(req);
        
        assertEquals(SuitabilityStatus.UNSUITABLE, result.status());
    }
    
    @Test
    void whenConflictingFertilizerCropWithSoilData_thenConditionallySuitable() {
        UUID plotId = UUID.randomUUID();
        SoilTest mockSoil = new SoilTest();
        when(soilTestRepository.findByPlotId(plotId)).thenReturn(List.of(mockSoil));
        
        CropSuitabilityRequest req = new CropSuitabilityRequest(UUID.randomUUID(), plotId, "ConflictingFertilizerCrop", LocalDate.now(), "Rabi");
        CropSuitabilityResult result = engine.evaluate(req);
        
        assertEquals(SuitabilityStatus.CONDITIONALLY_SUITABLE, result.status());
    }
}
""", is_test=True)

write_file("service/RegulatoryGateTest.java", """
package com.balanceepitome.agri.service;

import com.balanceepitome.agri.service.impl.SimpleRegulatoryGate;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class RegulatoryGateTest {
    
    private final RegulatoryGate gate = new SimpleRegulatoryGate();
    
    @Test
    void whenApprovedChemical_thenApproved() {
        RegulatoryDecision decision = gate.check("azadirachtin", "Tomato", "Aphids", "Karnataka");
        assertEquals(DecisionStatus.APPROVED, decision.status());
    }
    
    @Test
    void whenBannedChemical_thenBanned() {
        RegulatoryDecision decision = gate.check("monocrotophos", "Cotton", "Bollworm", "Karnataka");
        assertEquals(DecisionStatus.BANNED, decision.status());
    }
    
    @Test
    void whenUnknownChemical_thenUnknown() {
        RegulatoryDecision decision = gate.check("unknown_chemical", "Rice", "Stem Borer", "Karnataka");
        assertEquals(DecisionStatus.UNKNOWN, decision.status());
    }
}
""", is_test=True)

print("Java files generated.")
