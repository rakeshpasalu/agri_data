package com.balanceepitome.agri.repository;

import com.balanceepitome.agri.domain.crop.Crop;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;
import java.util.Optional;

public interface CropRepository extends JpaRepository<Crop, UUID> {
    Optional<Crop> findByCanonicalNameIgnoreCase(String canonicalName);
}
