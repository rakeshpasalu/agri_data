package com.balanceepitome.agri.repository;

import com.balanceepitome.agri.domain.evidence.KnowledgeRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;
import java.util.List;

public interface KnowledgeRecordRepository extends JpaRepository<KnowledgeRecord, UUID> {
    List<KnowledgeRecord> findByCategory(String category);
}
