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
