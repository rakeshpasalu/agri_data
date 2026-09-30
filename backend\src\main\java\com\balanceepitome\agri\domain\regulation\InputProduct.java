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
