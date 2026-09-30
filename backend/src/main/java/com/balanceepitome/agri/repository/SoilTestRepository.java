package com.balanceepitome.agri.repository;

import com.balanceepitome.agri.domain.farm.SoilTest;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;
import java.util.List;

public interface SoilTestRepository extends JpaRepository<SoilTest, UUID> {
    List<SoilTest> findByPlotId(UUID plotId);
}
