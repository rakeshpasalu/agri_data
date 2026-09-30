package com.balanceepitome.agri.repository;

import com.balanceepitome.agri.domain.farm.Plot;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;

public interface PlotRepository extends JpaRepository<Plot, UUID> {
}
