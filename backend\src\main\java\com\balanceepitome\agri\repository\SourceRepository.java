package com.balanceepitome.agri.repository;

import com.balanceepitome.agri.domain.evidence.Source;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;

public interface SourceRepository extends JpaRepository<Source, UUID> {}
