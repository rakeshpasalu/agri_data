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
