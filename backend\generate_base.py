import os

base_dir = r"c:\Users\pasal\Downloads\balance_epitome\backend"

def write_file(path, content):
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# pom.xml
write_file("pom.xml", """
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.0</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.balanceepitome</groupId>
    <artifactId>agri-backend</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>agri-backend</name>
    <description>Agricultural Intelligence Platform</description>
    <properties>
        <java.version>21</java.version>
        <hibernate.version>6.5.2.Final</hibernate.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.flywaydb</groupId>
            <artifactId>flyway-core</artifactId>
        </dependency>
        <dependency>
            <groupId>org.flywaydb</groupId>
            <artifactId>flyway-database-postgresql</artifactId>
        </dependency>
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.hibernate.orm</groupId>
            <artifactId>hibernate-spatial</artifactId>
            <version>${hibernate.version}</version>
        </dependency>
        <!-- https://mvnrepository.com/artifact/io.hypersistence/hypersistence-utils-hibernate-63 -->
        <dependency>
            <groupId>io.hypersistence</groupId>
            <artifactId>hypersistence-utils-hibernate-63</artifactId>
            <version>3.7.3</version>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-testcontainers</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.testcontainers</groupId>
            <artifactId>junit-jupiter</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.testcontainers</groupId>
            <artifactId>postgresql</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <excludes>
                        <exclude>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                        </exclude>
                    </excludes>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
""")

# application.yml
write_file("src/main/resources/application.yml", """
spring:
  application:
    name: agri-backend
  datasource:
    url: ${DB_URL:jdbc:postgresql://localhost:5432/agridb}
    username: ${DB_USER:postgres}
    password: ${DB_PASSWORD:postgres}
  jpa:
    hibernate:
      ddl-auto: validate
    properties:
      hibernate:
        dialect: org.hibernate.spatial.dialect.postgis.PostgisDialect
        format_sql: true
    show-sql: false
  flyway:
    enabled: true
    baseline-on-migrate: true

server:
  port: 8080

logging:
  level:
    root: INFO
    com.balanceepitome.agri: DEBUG
""")

# V1__core_schema.sql
write_file("src/main/resources/db/migration/V1__core_schema.sql", """
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TYPE data_provenance AS ENUM ('FARMER_ENTERED', 'FARM_MEASURED', 'GOVERNMENT_DATA', 'SCIENTIFIC_DATASET', 'SATELLITE_DERIVED', 'MODEL_DERIVED', 'REGIONAL_INFERENCE', 'DEMO_ONLY');
CREATE TYPE regulatory_status AS ENUM ('REGISTERED', 'RESTRICTED', 'BANNED', 'NOT_REGISTERED', 'WITHDRAWN', 'UNKNOWN');
CREATE TYPE observation_type AS ENUM ('FIELD_OBSERVATION', 'LABORATORY_ANALYSIS', 'SATELLITE_DERIVED', 'MODEL_OUTPUT', 'SURVEY_DATA', 'EXPERT_OPINION');
CREATE TYPE crop_cycle_status AS ENUM ('PLANNED', 'SOWN', 'GROWING', 'HARVESTING', 'HARVESTED', 'FAILED', 'ABANDONED');
CREATE TYPE management_type AS ENUM ('CULTURAL', 'MECHANICAL', 'BIOLOGICAL', 'CHEMICAL', 'INTEGRATED');
CREATE TYPE license_band AS ENUM ('GREEN', 'YELLOW', 'RED');
CREATE TYPE geographic_resolution AS ENUM ('NATIONAL', 'STATE', 'ZONE', 'DISTRICT', 'TALUK', 'VILLAGE', 'FARM', 'PLOT');
CREATE TYPE water_source_type AS ENUM ('BOREWELL', 'OPEN_WELL', 'CANAL', 'POND', 'LAKE', 'RAINFED');

-- Evidence & Knowledge System
CREATE TABLE source (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    authority_level VARCHAR(50),
    url VARCHAR(512),
    publication_date DATE,
    geographic_scope VARCHAR(255),
    license_band license_band,
    retrieved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE evidence (
    id UUID PRIMARY KEY,
    source_id UUID REFERENCES source(id),
    document_url VARCHAR(512),
    document_hash VARCHAR(255),
    page_reference VARCHAR(50),
    claim_text TEXT,
    geographic_applicability JSONB,
    observation_type observation_type,
    verified BOOLEAN DEFAULT FALSE,
    verification_date TIMESTAMP WITH TIME ZONE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE knowledge_record (
    id UUID PRIMARY KEY,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    conditions JSONB,
    content JSONB,
    evidence_id UUID REFERENCES evidence(id),
    geographic_resolution geographic_resolution,
    valid_from DATE,
    valid_until DATE,
    superseded_by UUID,
    confidence VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE knowledge_version (
    id UUID PRIMARY KEY,
    knowledge_record_id UUID REFERENCES knowledge_record(id),
    version_number INT,
    changed_by VARCHAR(255),
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    change_reason TEXT,
    previous_content JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE conflicting_evidence (
    id UUID PRIMARY KEY,
    knowledge_record_a_id UUID REFERENCES knowledge_record(id),
    knowledge_record_b_id UUID REFERENCES knowledge_record(id),
    conflict_type VARCHAR(100),
    resolution_status VARCHAR(50),
    resolution_notes TEXT,
    conditions_differ JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Farm Digital Twin
CREATE TABLE farmer (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone_hash VARCHAR(255),
    preferred_language VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE farm (
    id UUID PRIMARY KEY,
    farmer_id UUID REFERENCES farmer(id),
    name VARCHAR(255),
    location GEOMETRY(Point, 4326),
    boundary GEOMETRY(Polygon, 4326),
    area_hectares DECIMAL(10,4),
    survey_number VARCHAR(100),
    village_code VARCHAR(100),
    taluk VARCHAR(100),
    district VARCHAR(100),
    state VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE plot (
    id UUID PRIMARY KEY,
    farm_id UUID REFERENCES farm(id),
    name VARCHAR(255),
    boundary GEOMETRY(Polygon, 4326),
    area_hectares DECIMAL(10,4),
    soil_type VARCHAR(100),
    irrigation_type VARCHAR(100),
    water_source VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE soil_test (
    id UUID PRIMARY KEY,
    plot_id UUID REFERENCES plot(id),
    test_date DATE,
    ph DECIMAL(4,2),
    ec_dsm DECIMAL(6,2),
    organic_carbon_pct DECIMAL(5,2),
    nitrogen_kgha DECIMAL(8,2),
    phosphorus_kgha DECIMAL(8,2),
    potassium_kgha DECIMAL(8,2),
    zinc_ppm DECIMAL(6,2),
    iron_ppm DECIMAL(6,2),
    manganese_ppm DECIMAL(6,2),
    copper_ppm DECIMAL(6,2),
    boron_ppm DECIMAL(6,2),
    sulphur_kgha DECIMAL(8,2),
    lab_name VARCHAR(255),
    shc_id VARCHAR(100),
    data_provenance data_provenance,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE water_source (
    id UUID PRIMARY KEY,
    farm_id UUID REFERENCES farm(id),
    type water_source_type,
    depth_meters DECIMAL(6,2),
    discharge_lpm DECIMAL(8,2),
    quality_class VARCHAR(50),
    tested_date DATE,
    data_provenance data_provenance,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crop Knowledge
CREATE TABLE crop (
    id UUID PRIMARY KEY,
    canonical_name VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255),
    crop_type VARCHAR(100),
    crop_group VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE crop_name_mapping (
    id UUID PRIMARY KEY,
    crop_id UUID REFERENCES crop(id),
    language_code VARCHAR(10),
    name VARCHAR(255) NOT NULL,
    script VARCHAR(50),
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE crop_variety (
    id UUID PRIMARY KEY,
    crop_id UUID REFERENCES crop(id),
    variety_name VARCHAR(255) NOT NULL,
    released_by VARCHAR(255),
    release_year INT,
    duration_days_min INT,
    duration_days_max INT,
    season VARCHAR(100),
    characteristics JSONB,
    source_id UUID REFERENCES source(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE crop_requirement (
    id UUID PRIMARY KEY,
    crop_id UUID REFERENCES crop(id),
    variety_id UUID REFERENCES crop_variety(id),
    parameter VARCHAR(100),
    min_value DECIMAL(10,2),
    max_value DECIMAL(10,2),
    unit VARCHAR(50),
    condition JSONB,
    evidence_id UUID REFERENCES evidence(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE crop_calendar (
    id UUID PRIMARY KEY,
    crop_id UUID REFERENCES crop(id),
    zone VARCHAR(100),
    season VARCHAR(100),
    sowing_start_month INT,
    sowing_end_month INT,
    harvest_start_month INT,
    harvest_end_month INT,
    evidence_id UUID REFERENCES evidence(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crop Cycle (Farm Activity)
CREATE TABLE crop_cycle (
    id UUID PRIMARY KEY,
    plot_id UUID REFERENCES plot(id),
    crop_id UUID REFERENCES crop(id),
    variety_id UUID REFERENCES crop_variety(id),
    season VARCHAR(100),
    sowing_date DATE,
    expected_harvest_date DATE,
    actual_harvest_date DATE,
    status crop_cycle_status,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE farm_activity (
    id UUID PRIMARY KEY,
    crop_cycle_id UUID REFERENCES crop_cycle(id),
    activity_type VARCHAR(100),
    activity_date DATE,
    description TEXT,
    input_product VARCHAR(255),
    quantity DECIMAL(10,2),
    unit VARCHAR(50),
    cost_inr DECIMAL(10,2),
    data_provenance data_provenance,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE farm_observation (
    id UUID PRIMARY KEY,
    crop_cycle_id UUID REFERENCES crop_cycle(id),
    observation_date DATE,
    category VARCHAR(100),
    description TEXT,
    severity VARCHAR(50),
    photo_url VARCHAR(512),
    data_provenance data_provenance,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE harvest (
    id UUID PRIMARY KEY,
    crop_cycle_id UUID REFERENCES crop_cycle(id),
    harvest_date DATE,
    quantity_kg DECIMAL(12,2),
    quality_grade VARCHAR(50),
    data_provenance data_provenance,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sale (
    id UUID PRIMARY KEY,
    harvest_id UUID REFERENCES harvest(id),
    sale_date DATE,
    market_name VARCHAR(255),
    buyer_type VARCHAR(100),
    price_per_kg_inr DECIMAL(10,2),
    quantity_kg DECIMAL(12,2),
    transport_cost_inr DECIMAL(10,2),
    commission_inr DECIMAL(10,2),
    data_provenance data_provenance,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE expense (
    id UUID PRIMARY KEY,
    crop_cycle_id UUID REFERENCES crop_cycle(id),
    category VARCHAR(100),
    description TEXT,
    amount_inr DECIMAL(10,2),
    expense_date DATE,
    data_provenance data_provenance,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Nutrient Recommendations
CREATE TABLE nutrient_recommendation (
    id UUID PRIMARY KEY,
    crop_id UUID REFERENCES crop(id),
    variety_id UUID REFERENCES crop_variety(id),
    soil_type VARCHAR(100),
    irrigation_status VARCHAR(100),
    zone VARCHAR(100),
    n_kgha DECIMAL(8,2),
    p2o5_kgha DECIMAL(8,2),
    k2o_kgha DECIMAL(8,2),
    other_inputs JSONB,
    evidence_id UUID REFERENCES evidence(id),
    conditions JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Pest & Disease
CREATE TABLE pest (
    id UUID PRIMARY KEY,
    canonical_name VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255),
    pest_type VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE disease (
    id UUID PRIMARY KEY,
    canonical_name VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255),
    causal_agent VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pest_crop_association (
    id UUID PRIMARY KEY,
    pest_id UUID REFERENCES pest(id),
    crop_id UUID REFERENCES crop(id),
    severity_typical VARCHAR(50),
    season VARCHAR(100),
    geographic_scope VARCHAR(255),
    evidence_id UUID REFERENCES evidence(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE disease_crop_association (
    id UUID PRIMARY KEY,
    disease_id UUID REFERENCES disease(id),
    crop_id UUID REFERENCES crop(id),
    severity_typical VARCHAR(50),
    season VARCHAR(100),
    geographic_scope VARCHAR(255),
    evidence_id UUID REFERENCES evidence(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pest_management (
    id UUID PRIMARY KEY,
    pest_id UUID REFERENCES pest(id),
    crop_id UUID REFERENCES crop(id),
    management_type management_type,
    description TEXT,
    active_ingredient VARCHAR(255),
    formulation VARCHAR(255),
    dose DECIMAL(10,2),
    dose_unit VARCHAR(50),
    phi_days INT,
    evidence_id UUID REFERENCES evidence(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE disease_management (
    id UUID PRIMARY KEY,
    disease_id UUID REFERENCES disease(id),
    crop_id UUID REFERENCES crop(id),
    management_type management_type,
    description TEXT,
    active_ingredient VARCHAR(255),
    formulation VARCHAR(255),
    dose DECIMAL(10,2),
    dose_unit VARCHAR(50),
    phi_days INT,
    evidence_id UUID REFERENCES evidence(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Regulatory
CREATE TABLE input_product (
    id UUID PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    active_ingredient VARCHAR(255),
    formulation_type VARCHAR(100),
    manufacturer VARCHAR(255),
    cibrc_registration_number VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE input_regulation (
    id UUID PRIMARY KEY,
    input_product_id UUID REFERENCES input_product(id),
    regulatory_status regulatory_status,
    effective_date DATE,
    expiry_date DATE,
    applicable_crops TEXT[],
    applicable_pests TEXT[],
    source_id UUID REFERENCES source(id),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Market
CREATE TABLE market (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    market_type VARCHAR(100),
    location GEOMETRY(Point, 4326),
    district VARCHAR(100),
    state VARCHAR(100),
    agmarknet_code VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE market_price (
    id UUID PRIMARY KEY,
    market_id UUID REFERENCES market(id),
    commodity VARCHAR(255),
    variety VARCHAR(255),
    grade VARCHAR(100),
    arrival_quantity DECIMAL(12,2),
    min_price_per_quintal DECIMAL(10,2),
    max_price_per_quintal DECIMAL(10,2),
    modal_price_per_quintal DECIMAL(10,2),
    price_date DATE,
    source_id UUID REFERENCES source(id),
    retrieved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Weather
CREATE TABLE weather_observation (
    id UUID PRIMARY KEY,
    location GEOMETRY(Point, 4326),
    observation_date DATE,
    observation_type VARCHAR(100),
    temperature_max_c DECIMAL(5,2),
    temperature_min_c DECIMAL(5,2),
    temperature_mean_c DECIMAL(5,2),
    rainfall_mm DECIMAL(6,2),
    humidity_pct DECIMAL(5,2),
    wind_speed_ms DECIMAL(5,2),
    solar_radiation_mjm2 DECIMAL(6,2),
    et0_mm DECIMAL(6,2),
    provider VARCHAR(100),
    retrieved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Multilingual
CREATE TABLE agricultural_term (
    id UUID PRIMARY KEY,
    canonical_key VARCHAR(255) UNIQUE NOT NULL,
    category VARCHAR(100),
    english_term VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE agricultural_term_translation (
    id UUID PRIMARY KEY,
    term_id UUID REFERENCES agricultural_term(id),
    language_code VARCHAR(10),
    translated_term VARCHAR(255) NOT NULL,
    script VARCHAR(50),
    romanized VARCHAR(255),
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
""")

print("Files generated.")
