package com.balanceepitome.agri.repository;

import com.balanceepitome.agri.domain.crop.CropVariety;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;
import java.util.List;

public interface CropVarietyRepository extends JpaRepository<CropVariety, UUID> {
    List<CropVariety> findByCropId(UUID cropId);
}
