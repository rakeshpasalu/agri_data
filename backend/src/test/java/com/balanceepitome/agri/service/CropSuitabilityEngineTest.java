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
