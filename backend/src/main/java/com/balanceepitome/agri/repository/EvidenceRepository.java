package com.balanceepitome.agri.repository;

import com.balanceepitome.agri.domain.evidence.Evidence;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;

public interface EvidenceRepository extends JpaRepository<Evidence, UUID> {}
