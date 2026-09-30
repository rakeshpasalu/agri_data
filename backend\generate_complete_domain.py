import os

base_dir = r"c:\Users\pasal\Downloads\balance_epitome\backend\src\main\java\com\balanceepitome\agri"
test_dir = r"c:\Users\pasal\Downloads\balance_epitome\backend\src\test\java\com\balanceepitome\agri"

def write_file(rel_path, content, is_test=False):
    root = test_dir if is_test else base_dir
    full_path = os.path.join(root, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote {rel_path}")

# =========================================================================
# EVIDENCE DOMAIN
# =========================================================================
write_file("domain/evidence/Source.java", """
package com.balanceepitome.agri.domain.evidence;

import com.balanceepitome.agri.domain.common.LicenseBand;
import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "source")
@Data
public class Source {
    @Id
    private UUID id;
    
    @Column(nullable = false)
    private String name;
    
    private String authorityLevel;
    private String url;
    private LocalDate publicationDate;
    private String geographicScope;
    
    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "license_band")
    private LicenseBand licenseBand;
    
    private ZonedDateTime retrievedAt;
    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/evidence/Evidence.java", """
package com.balanceepitome.agri.domain.evidence;

import com.balanceepitome.agri.domain.common.ObservationType;
import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
import java.time.ZonedDateTime;
import java.util.Map;
import java.util.UUID;

@Entity
@Table(name = "evidence")
@Data
public class Evidence {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "source_id")
    private Source source;

    private String documentUrl;
    private String documentHash;
    private String pageReference;

    @Column(columnDefinition = "TEXT")
    private String claimText;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> geographicApplicability;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "observation_type")
    private ObservationType observationType;

    private Boolean verified;
    private ZonedDateTime verificationDate;

    @Column(columnDefinition = "TEXT")
    private String notes;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/evidence/KnowledgeRecord.java", """
package com.balanceepitome.agri.domain.evidence;

import com.balanceepitome.agri.domain.common.GeographicResolution;
import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.Map;
import java.util.UUID;

@Entity
@Table(name = "knowledge_record")
@Data
public class KnowledgeRecord {
    @Id
    private UUID id;

    private String category;
    private String subcategory;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> conditions;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> content;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "evidence_id")
    private Evidence evidence;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "geographic_resolution")
    private GeographicResolution geographicResolution;

    private LocalDate validFrom;
    private LocalDate validUntil;
    private UUID supersededBy;
    private String confidence;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/evidence/KnowledgeVersion.java", """
package com.balanceepitome.agri.domain.evidence;

import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
import java.time.ZonedDateTime;
import java.util.Map;
import java.util.UUID;

@Entity
@Table(name = "knowledge_version")
@Data
public class KnowledgeVersion {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "knowledge_record_id")
    private KnowledgeRecord knowledgeRecord;

    private Integer versionNumber;
    private String changedBy;
    private ZonedDateTime changedAt;
    
    @Column(columnDefinition = "TEXT")
    private String changeReason;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> previousContent;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/evidence/ConflictingEvidence.java", """
package com.balanceepitome.agri.domain.evidence;

import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
import java.time.ZonedDateTime;
import java.util.Map;
import java.util.UUID;

@Entity
@Table(name = "conflicting_evidence")
@Data
public class ConflictingEvidence {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "knowledge_record_a_id")
    private KnowledgeRecord knowledgeRecordA;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "knowledge_record_b_id")
    private KnowledgeRecord knowledgeRecordB;

    private String conflictType;
    private String resolutionStatus;
    
    @Column(columnDefinition = "TEXT")
    private String resolutionNotes;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> conditionsDiffer;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

# =========================================================================
# FARM DOMAIN EXTENSIONS
# =========================================================================
write_file("domain/farm/Farmer.java", """
package com.balanceepitome.agri.domain.farm;

import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "farmer")
@Data
public class Farmer {
    @Id
    private UUID id;

    @Column(nullable = false)
    private String name;

    private String phoneHash;
    private String preferredLanguage;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/farm/WaterSource.java", """
package com.balanceepitome.agri.domain.farm;

import com.balanceepitome.agri.domain.common.DataProvenance;
import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "water_source")
@Data
public class WaterSource {
    @Id
    private UUID id;

    @Column(name = "farm_id")
    private UUID farmId;

    private String type;
    private BigDecimal depthMeters;
    private BigDecimal dischargeLpm;
    private String qualityClass;
    private LocalDate testedDate;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "data_provenance")
    private DataProvenance dataProvenance;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/farm/FarmPhoto.java", """
package com.balanceepitome.agri.domain.farm;

import com.balanceepitome.agri.domain.common.DataProvenance;
import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "farm_photo")
@Data
public class FarmPhoto {
    @Id
    private UUID id;

    @Column(name = "plot_id")
    private UUID plotId;

    private String photoUrl;
    private String caption;
    private String tags;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "data_provenance")
    private DataProvenance dataProvenance;

    private ZonedDateTime capturedAt;
    private ZonedDateTime createdAt;
}
""")

write_file("domain/farm/FarmerFeedback.java", """
package com.balanceepitome.agri.domain.farm;

import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "farmer_feedback")
@Data
public class FarmerFeedback {
    @Id
    private UUID id;

    @Column(name = "farmer_id")
    private UUID farmerId;

    private UUID recommendationId;
    private Integer rating;
    
    @Column(columnDefinition = "TEXT")
    private String comment;
    
    private Boolean adopted;
    private ZonedDateTime createdAt;
}
""")

write_file("domain/farm/AgronomistReview.java", """
package com.balanceepitome.agri.domain.farm;

import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "agronomist_review")
@Data
public class AgronomistReview {
    @Id
    private UUID id;

    private UUID recommendationId;
    private String reviewerName;
    private String reviewerOrganization;
    private String reviewStatus; // APPROVED, REVISED, REJECTED
    
    @Column(columnDefinition = "TEXT")
    private String notes;

    private ZonedDateTime reviewedAt;
    private ZonedDateTime createdAt;
}
""")

# =========================================================================
# CROP DOMAIN
# =========================================================================
write_file("domain/crop/Crop.java", """
package com.balanceepitome.agri.domain.crop;

import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "crop")
@Data
public class Crop {
    @Id
    private UUID id;

    @Column(nullable = false)
    private String canonicalName;

    private String scientificName;
    private String cropType;
    private String cropGroup;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/crop/CropVariety.java", """
package com.balanceepitome.agri.domain.crop;

import com.balanceepitome.agri.domain.evidence.Source;
import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
import java.time.ZonedDateTime;
import java.util.Map;
import java.util.UUID;

@Entity
@Table(name = "crop_variety")
@Data
public class CropVariety {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_id")
    private Crop crop;

    @Column(nullable = false)
    private String varietyName;

    private String releasedBy;
    private Integer releaseYear;
    private Integer durationDaysMin;
    private Integer durationDaysMax;
    private String season;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> characteristics;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "source_id")
    private Source source;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/crop/CropRequirement.java", """
package com.balanceepitome.agri.domain.crop;

import com.balanceepitome.agri.domain.evidence.Evidence;
import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
import java.math.BigDecimal;
import java.time.ZonedDateTime;
import java.util.Map;
import java.util.UUID;

@Entity
@Table(name = "crop_requirement")
@Data
public class CropRequirement {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_id")
    private Crop crop;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "variety_id")
    private CropVariety variety;

    private String parameter;
    private BigDecimal minValue;
    private BigDecimal maxValue;
    private String unit;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> condition;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "evidence_id")
    private Evidence evidence;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/crop/CropCalendar.java", """
package com.balanceepitome.agri.domain.crop;

import com.balanceepitome.agri.domain.evidence.Evidence;
import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "crop_calendar")
@Data
public class CropCalendar {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_id")
    private Crop crop;

    private String zone;
    private String season;
    private Integer sowingStartMonth;
    private Integer sowingEndMonth;
    private Integer harvestStartMonth;
    private Integer harvestEndMonth;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "evidence_id")
    private Evidence evidence;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/crop/CropNameMapping.java", """
package com.balanceepitome.agri.domain.crop;

import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "crop_name_mapping")
@Data
public class CropNameMapping {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_id")
    private Crop crop;

    private String languageCode;
    private String name;
    private String script;
    private Boolean isPrimary;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/crop/AgriculturalProtocol.java", """
package com.balanceepitome.agri.domain.crop;

import com.balanceepitome.agri.domain.evidence.Evidence;
import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
import java.time.ZonedDateTime;
import java.util.Map;
import java.util.UUID;

@Entity
@Table(name = "agricultural_protocol")
@Data
public class AgriculturalProtocol {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_id")
    private Crop crop;

    private String stageName;
    private Integer daysAfterSowingMin;
    private Integer daysAfterSowingMax;
    
    @Column(columnDefinition = "TEXT")
    private String protocolDescription;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> inputDetails;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "evidence_id")
    private Evidence evidence;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

# =========================================================================
# SEED DOMAIN
# =========================================================================
write_file("domain/seed/SeedProduct.java", """
package com.balanceepitome.agri.domain.seed;

import com.balanceepitome.agri.domain.crop.CropVariety;
import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "seed_product")
@Data
public class SeedProduct {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "variety_id")
    private CropVariety variety;

    private String brandName;
    private String certificationClass; // FOUNDATION, CERTIFIED, TRUTHFULLY_LABELED
    private BigDecimal packSizeKg;
    private BigDecimal mrpInr;
    private Boolean verifiedAvailable;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/seed/SeedSupplier.java", """
package com.balanceepitome.agri.domain.seed;

import jakarta.persistence.*;
import lombok.Data;
import org.locationtech.jts.geom.Point;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "seed_supplier")
@Data
public class SeedSupplier {
    @Id
    private UUID id;

    private String name;
    private String supplierType; // KSSC_OUTLET, RSK, COOPERATIVE, PRIVATE_DEALER
    private String contactNumber;
    private String address;
    private String taluk;
    private String district;

    @Column(columnDefinition = "geometry(Point, 4326)")
    private Point location;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

# =========================================================================
# CROP CYCLE DOMAIN
# =========================================================================
write_file("domain/cropcycle/CropCycle.java", """
package com.balanceepitome.agri.domain.cropcycle;

import com.balanceepitome.agri.domain.common.CropCycleStatus;
import com.balanceepitome.agri.domain.crop.Crop;
import com.balanceepitome.agri.domain.crop.CropVariety;
import com.balanceepitome.agri.domain.farm.Plot;
import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "crop_cycle")
@Data
public class CropCycle {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "plot_id")
    private Plot plot;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_id")
    private Crop crop;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "variety_id")
    private CropVariety variety;

    private String season;
    private LocalDate sowingDate;
    private LocalDate expectedHarvestDate;
    private LocalDate actualHarvestDate;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "crop_cycle_status")
    private CropCycleStatus status;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/cropcycle/FarmActivity.java", """
package com.balanceepitome.agri.domain.cropcycle;

import com.balanceepitome.agri.domain.common.DataProvenance;
import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "farm_activity")
@Data
public class FarmActivity {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_cycle_id")
    private CropCycle cropCycle;

    private String activityType;
    private LocalDate activityDate;
    
    @Column(columnDefinition = "TEXT")
    private String description;
    
    private String inputProduct;
    private BigDecimal quantity;
    private String unit;
    private BigDecimal costInr;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "data_provenance")
    private DataProvenance dataProvenance;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/cropcycle/FarmObservation.java", """
package com.balanceepitome.agri.domain.cropcycle;

import com.balanceepitome.agri.domain.common.DataProvenance;
import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "farm_observation")
@Data
public class FarmObservation {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_cycle_id")
    private CropCycle cropCycle;

    private LocalDate observationDate;
    private String category;
    
    @Column(columnDefinition = "TEXT")
    private String description;
    
    private String severity;
    private String photoUrl;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "data_provenance")
    private DataProvenance dataProvenance;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/cropcycle/Harvest.java", """
package com.balanceepitome.agri.domain.cropcycle;

import com.balanceepitome.agri.domain.common.DataProvenance;
import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "harvest")
@Data
public class Harvest {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_cycle_id")
    private CropCycle cropCycle;

    private LocalDate harvestDate;
    private BigDecimal quantityKg;
    private String qualityGrade;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "data_provenance")
    private DataProvenance dataProvenance;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/cropcycle/Sale.java", """
package com.balanceepitome.agri.domain.cropcycle;

import com.balanceepitome.agri.domain.common.DataProvenance;
import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "sale")
@Data
public class Sale {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "harvest_id")
    private Harvest harvest;

    private LocalDate saleDate;
    private String marketName;
    private String buyerType;
    private BigDecimal pricePerKgInr;
    private BigDecimal quantityKg;
    private BigDecimal transportCostInr;
    private BigDecimal commissionInr;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "data_provenance")
    private DataProvenance dataProvenance;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/cropcycle/Expense.java", """
package com.balanceepitome.agri.domain.cropcycle;

import com.balanceepitome.agri.domain.common.DataProvenance;
import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "expense")
@Data
public class Expense {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_cycle_id")
    private CropCycle cropCycle;

    private String category;
    
    @Column(columnDefinition = "TEXT")
    private String description;
    
    private BigDecimal amountInr;
    private LocalDate expenseDate;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "data_provenance")
    private DataProvenance dataProvenance;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

# =========================================================================
# NUTRIENT DOMAIN
# =========================================================================
write_file("domain/nutrient/NutrientRecommendation.java", """
package com.balanceepitome.agri.domain.nutrient;

import com.balanceepitome.agri.domain.crop.Crop;
import com.balanceepitome.agri.domain.crop.CropVariety;
import com.balanceepitome.agri.domain.evidence.Evidence;
import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
import java.math.BigDecimal;
import java.time.ZonedDateTime;
import java.util.Map;
import java.util.UUID;

@Entity
@Table(name = "nutrient_recommendation")
@Data
public class NutrientRecommendation {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_id")
    private Crop crop;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "variety_id")
    private CropVariety variety;

    private String soilType;
    private String irrigationStatus;
    private String zone;

    private BigDecimal nKgha;
    private BigDecimal p2o5Kgha;
    private BigDecimal k2oKgha;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> otherInputs;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "evidence_id")
    private Evidence evidence;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> conditions;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

# =========================================================================
# PEST & DISEASE DOMAIN
# =========================================================================
write_file("domain/pest/Pest.java", """
package com.balanceepitome.agri.domain.pest;

import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "pest")
@Data
public class Pest {
    @Id
    private UUID id;

    @Column(nullable = false)
    private String canonicalName;

    private String scientificName;
    private String pestType;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/pest/Disease.java", """
package com.balanceepitome.agri.domain.pest;

import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "disease")
@Data
public class Disease {
    @Id
    private UUID id;

    @Column(nullable = false)
    private String canonicalName;

    private String scientificName;
    private String causalAgent;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/pest/PestCropAssociation.java", """
package com.balanceepitome.agri.domain.pest;

import com.balanceepitome.agri.domain.crop.Crop;
import com.balanceepitome.agri.domain.evidence.Evidence;
import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "pest_crop_association")
@Data
public class PestCropAssociation {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "pest_id")
    private Pest pest;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_id")
    private Crop crop;

    private String severityTypical;
    private String season;
    private String geographicScope;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "evidence_id")
    private Evidence evidence;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/pest/DiseaseCropAssociation.java", """
package com.balanceepitome.agri.domain.pest;

import com.balanceepitome.agri.domain.crop.Crop;
import com.balanceepitome.agri.domain.evidence.Evidence;
import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "disease_crop_association")
@Data
public class DiseaseCropAssociation {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "disease_id")
    private Disease disease;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_id")
    private Crop crop;

    private String severityTypical;
    private String season;
    private String geographicScope;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "evidence_id")
    private Evidence evidence;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/pest/PestManagement.java", """
package com.balanceepitome.agri.domain.pest;

import com.balanceepitome.agri.domain.common.ManagementType;
import com.balanceepitome.agri.domain.crop.Crop;
import com.balanceepitome.agri.domain.evidence.Evidence;
import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "pest_management")
@Data
public class PestManagement {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "pest_id")
    private Pest pest;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_id")
    private Crop crop;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "management_type")
    private ManagementType managementType;

    @Column(columnDefinition = "TEXT")
    private String description;

    private String activeIngredient;
    private String formulation;
    private BigDecimal dose;
    private String doseUnit;
    private Integer phiDays;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "evidence_id")
    private Evidence evidence;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/pest/DiseaseManagement.java", """
package com.balanceepitome.agri.domain.pest;

import com.balanceepitome.agri.domain.common.ManagementType;
import com.balanceepitome.agri.domain.crop.Crop;
import com.balanceepitome.agri.domain.evidence.Evidence;
import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "disease_management")
@Data
public class DiseaseManagement {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "disease_id")
    private Disease disease;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crop_id")
    private Crop crop;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "management_type")
    private ManagementType managementType;

    @Column(columnDefinition = "TEXT")
    private String description;

    private String activeIngredient;
    private String formulation;
    private BigDecimal dose;
    private String doseUnit;
    private Integer phiDays;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "evidence_id")
    private Evidence evidence;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

# =========================================================================
# REGULATORY DOMAIN
# =========================================================================
write_file("domain/regulation/InputProduct.java", """
package com.balanceepitome.agri.domain.regulation;

import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "input_product")
@Data
public class InputProduct {
    @Id
    private UUID id;

    @Column(nullable = false)
    private String productName;

    private String activeIngredient;
    private String formulationType;
    private String manufacturer;
    private String cibrcRegistrationNumber;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/regulation/InputRegulation.java", """
package com.balanceepitome.agri.domain.regulation;

import com.balanceepitome.agri.domain.common.RegulatoryStatus;
import com.balanceepitome.agri.domain.evidence.Source;
import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "input_regulation")
@Data
public class InputRegulation {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "input_product_id")
    private InputProduct inputProduct;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "regulatory_status")
    private RegulatoryStatus regulatoryStatus;

    private LocalDate effectiveDate;
    private LocalDate expiryDate;
    
    @Column(columnDefinition = "TEXT[]")
    private String[] applicableCrops;

    @Column(columnDefinition = "TEXT[]")
    private String[] applicablePests;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "source_id")
    private Source source;

    @Column(columnDefinition = "TEXT")
    private String notes;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

# =========================================================================
# MARKET DOMAIN
# =========================================================================
write_file("domain/market/Market.java", """
package com.balanceepitome.agri.domain.market;

import jakarta.persistence.*;
import lombok.Data;
import org.locationtech.jts.geom.Point;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "market")
@Data
public class Market {
    @Id
    private UUID id;

    @Column(nullable = false)
    private String name;

    private String marketType;

    @Column(columnDefinition = "geometry(Point, 4326)")
    private Point location;

    private String district;
    private String state;
    private String agmarknetCode;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/market/MarketPrice.java", """
package com.balanceepitome.agri.domain.market;

import com.balanceepitome.agri.domain.evidence.Source;
import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "market_price")
@Data
public class MarketPrice {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "market_id")
    private Market market;

    private String commodity;
    private String variety;
    private String grade;
    private BigDecimal arrivalQuantity;
    private BigDecimal minPricePerQuintal;
    private BigDecimal maxPricePerQuintal;
    private BigDecimal modalPricePerQuintal;
    private LocalDate priceDate;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "source_id")
    private Source source;

    private ZonedDateTime retrievedAt;
    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/market/MarketArrival.java", """
package com.balanceepitome.agri.domain.market;

import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "market_arrival")
@Data
public class MarketArrival {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "market_id")
    private Market market;

    private String commodity;
    private LocalDate arrivalDate;
    private BigDecimal quantityTonnes;
    private String unitOfMeasure;

    private ZonedDateTime createdAt;
}
""")

# =========================================================================
# WEATHER DOMAIN
# =========================================================================
write_file("domain/weather/WeatherObservation.java", """
package com.balanceepitome.agri.domain.weather;

import jakarta.persistence.*;
import lombok.Data;
import org.locationtech.jts.geom.Point;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "weather_observation")
@Data
public class WeatherObservation {
    @Id
    private UUID id;

    @Column(columnDefinition = "geometry(Point, 4326)")
    private Point location;

    private LocalDate observationDate;
    private String observationType; // HISTORICAL_REANALYSIS, STATION_OBSERVED, MODEL_FORECAST
    private BigDecimal temperatureMaxC;
    private BigDecimal temperatureMinC;
    private BigDecimal temperatureMeanC;
    private BigDecimal rainfallMm;
    private BigDecimal humidityPct;
    private BigDecimal windSpeedMs;
    private BigDecimal solarRadiationMjm2;
    private BigDecimal et0Mm;
    private String provider;

    private ZonedDateTime retrievedAt;
    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/weather/WeatherClimatology.java", """
package com.balanceepitome.agri.domain.weather;

import lombok.Builder;
import lombok.Data;
import java.math.BigDecimal;
import java.util.Map;

@Data
@Builder
public class WeatherClimatology {
    private String locationDescription;
    private BigDecimal elevationMeters;
    private BigDecimal annualMeanTempC;
    private BigDecimal annualPrecipitationMm;
    private Map<Integer, BigDecimal> monthlyPrecipitationMm;
    private Map<Integer, BigDecimal> monthlyMeanTempC;
    private String provider;
    private String baselinePeriod; // e.g., 2001-2020
}
""")

# =========================================================================
# MULTILINGUAL DOMAIN
# =========================================================================
write_file("domain/i18n/AgriculturalTerm.java", """
package com.balanceepitome.agri.domain.i18n;

import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "agricultural_term")
@Data
public class AgriculturalTerm {
    @Id
    private UUID id;

    @Column(nullable = false, unique = true)
    private String canonicalKey;

    private String category;
    private String englishTerm;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

write_file("domain/i18n/AgriculturalTermTranslation.java", """
package com.balanceepitome.agri.domain.i18n;

import jakarta.persistence.*;
import lombok.Data;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "agricultural_term_translation")
@Data
public class AgriculturalTermTranslation {
    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "term_id")
    private AgriculturalTerm term;

    private String languageCode;
    private String translatedTerm;
    private String script;
    private String romanized;
    private Boolean verified;

    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
""")

# =========================================================================
# RAG INTERFACES (Step 17 & 20)
# =========================================================================
write_file("service/rag/RagMetadata.java", """
package com.balanceepitome.agri.service.rag;

import java.time.LocalDate;
import java.util.List;

public record RagMetadata(
    String country,
    String region,
    String agroClimaticZone,
    String crop,
    String season,
    String topic,
    String authority,
    LocalDate publicationDate,
    LocalDate validUntil,
    String licenseBand,
    String language,
    List<String> keywords
) {}
""")

write_file("service/rag/EvidenceChunk.java", """
package com.balanceepitome.agri.service.rag;

import java.util.UUID;

public record EvidenceChunk(
    UUID chunkId,
    UUID sourceId,
    String sourceName,
    String documentTitle,
    String pageOrSection,
    String chunkText,
    RagMetadata metadata,
    double relevanceScore
) {}
""")

write_file("service/rag/RagSearchRequest.java", """
package com.balanceepitome.agri.service.rag;

public record RagSearchRequest(
    String query,
    String targetCrop,
    String targetZone,
    String targetSeason,
    String targetLanguage,
    int maxResults,
    boolean strictZoneFilter
) {}
""")

write_file("service/rag/RagService.java", """
package com.balanceepitome.agri.service.rag;

import java.util.List;

public interface RagService {
    List<EvidenceChunk> retrieveEvidence(RagSearchRequest request);
    void indexDocument(UUID sourceId, String content, RagMetadata metadata);
}
""")

# =========================================================================
# REPOSITORIES
# =========================================================================
write_file("repository/SourceRepository.java", """
package com.balanceepitome.agri.repository;

import com.balanceepitome.agri.domain.evidence.Source;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;

public interface SourceRepository extends JpaRepository<Source, UUID> {}
""")

write_file("repository/EvidenceRepository.java", """
package com.balanceepitome.agri.repository;

import com.balanceepitome.agri.domain.evidence.Evidence;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;

public interface EvidenceRepository extends JpaRepository<Evidence, UUID> {}
""")

write_file("repository/KnowledgeRecordRepository.java", """
package com.balanceepitome.agri.repository;

import com.balanceepitome.agri.domain.evidence.KnowledgeRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;
import java.util.List;

public interface KnowledgeRecordRepository extends JpaRepository<KnowledgeRecord, UUID> {
    List<KnowledgeRecord> findByCategory(String category);
}
""")

write_file("repository/CropRepository.java", """
package com.balanceepitome.agri.repository;

import com.balanceepitome.agri.domain.crop.Crop;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;
import java.util.Optional;

public interface CropRepository extends JpaRepository<Crop, UUID> {
    Optional<Crop> findByCanonicalNameIgnoreCase(String canonicalName);
}
""")

write_file("repository/CropVarietyRepository.java", """
package com.balanceepitome.agri.repository;

import com.balanceepitome.agri.domain.crop.CropVariety;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;
import java.util.List;

public interface CropVarietyRepository extends JpaRepository<CropVariety, UUID> {
    List<CropVariety> findByCropId(UUID cropId);
}
""")

# =========================================================================
# REST CONTROLLERS (Step 26: Developer/Admin Inspection API)
# =========================================================================
write_file("controller/AdminInspectionController.java", """
package com.balanceepitome.agri.controller;

import com.balanceepitome.agri.service.CropSuitabilityEngine;
import com.balanceepitome.agri.service.CropSuitabilityRequest;
import com.balanceepitome.agri.service.CropSuitabilityResult;
import com.balanceepitome.agri.service.RegulatoryGate;
import com.balanceepitome.agri.service.RegulatoryDecision;
import org.springframework.web.bind.annotation.*;
import java.util.Map;
import java.util.List;
import java.util.UUID;
import java.time.LocalDate;

@RestController
@RequestMapping("/api/admin")
@CrossOrigin(origins = "*")
public class AdminInspectionController {

    private final CropSuitabilityEngine cropSuitabilityEngine;
    private final RegulatoryGate regulatoryGate;

    public AdminInspectionController(CropSuitabilityEngine cropSuitabilityEngine, RegulatoryGate regulatoryGate) {
        this.cropSuitabilityEngine = cropSuitabilityEngine;
        this.regulatoryGate = regulatoryGate;
    }

    @GetMapping("/status")
    public Map<String, Object> getSystemStatus() {
        return Map.of(
            "system", "Agricultural Intelligence Platform (Precision Farming)",
            "pilotGeography", "India -> Karnataka -> Chitradurga -> Molakalmuru -> Hosanagalapura",
            "evidenceEngine", "Deterministic / Rule-Based",
            "regulatoryBoundary", "CIB&RC Strict Enforcement Active",
            "version", "0.1.0-FOUNDATION"
        );
    }

    @GetMapping("/sources")
    public List<Map<String, Object>> getSources() {
        return List.of(
            Map.of("name", "UAS Bangalore Package of Practices", "authority", "UNIVERSITY", "geo", "Zone IV (Central Dry Zone)", "license", "YELLOW"),
            Map.of("name", "CIB&RC Major Uses & Banned List", "authority", "GOVERNMENT", "geo", "National (India)", "license", "GREEN"),
            Map.of("name", "KSSC Variety Catalogue", "authority", "STATE_ENTERPRISE", "geo", "Karnataka", "license", "GREEN"),
            Map.of("name", "ICAR-NBSS&LUP Soil Survey of Chitradurga", "authority", "RESEARCH_INSTITUTION", "geo", "District", "license", "YELLOW"),
            Map.of("name", "NASA POWER Agroclimatology", "authority", "GOVERNMENT (NASA)", "geo", "Point Reanalysis ~14.887, 76.842", "license", "GREEN"),
            Map.of("name", "Kumar Naik et al. 2020 (n=148 samples)", "authority", "PEER_REVIEWED_JOURNAL", "geo", "Molakalmuru Taluk", "license", "YELLOW")
        );
    }

    @GetMapping("/conflicts")
    public List<Map<String, Object>> getDocumentedConflicts() {
        return List.of(
            Map.of(
                "conflictId", "CONFLICT-002",
                "crop", "Groundnut",
                "parameter", "NPK Recommended Dose of Fertilizer (RDF)",
                "sourceA", "UASB PoP: 25:75:37.5 NPK kg/ha + 500kg gypsum",
                "sourceB", "NARP / CDZ Table: 25:50:25 NPK kg/ha (rainfed)",
                "cause", "Difference in irrigation assumption (irrigated vs rainfed) & soil calcium",
                "resolutionPolicy", "CONFLICTING_EVIDENCE preserved. Do not average. Require farm soil test + STCR calibration."
            )
        );
    }

    @PostMapping("/evaluate-suitability")
    public CropSuitabilityResult evaluateSuitability(@RequestBody CropSuitabilityRequest request) {
        return cropSuitabilityEngine.evaluate(request);
    }

    @GetMapping("/check-regulation")
    public RegulatoryDecision checkRegulation(
            @RequestParam String activeIngredient,
            @RequestParam String crop,
            @RequestParam String pest,
            @RequestParam(defaultValue = "Karnataka") String geography) {
        return regulatoryGate.check(activeIngredient, crop, pest, geography);
    }
}
""")

print("Complete domain model, RAG interfaces, and REST controllers generated.")
