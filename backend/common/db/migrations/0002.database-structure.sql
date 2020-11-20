--
-- file: breviary/backend/common/db/migrations/0002.database-structure.sql
-- depends: 0001.initial-schema
--

CREATE TYPE SEX AS ENUM (
    'M',
    'F'
    );

CREATE TABLE patients_heparin
(
    id               BIGSERIAL   NOT NULL,
    first_name       TEXT,
    last_name        TEXT,
    date_of_birth    date,
    height           NUMERIC,
    weight           NUMERIC     NOT NULL,
    sex              SEX,
    target_aptt_low  NUMERIC     NOT NULL,
    target_aptt_high NUMERIC     NOT NULL,
    active           BOOLEAN     NOT NULL, -- default false, false means the patient is in IKEM DB but not in app DB
    other_params     jsonb,
    created_at       TIMESTAMPTZ NOT NULL,
    updated_at       TIMESTAMPTZ NOT NULL,
    deleted_at       TIMESTAMPTZ,
    CONSTRAINT pk_patients__id PRIMARY KEY (id)
);


CREATE TABLE aptt_values
(
    id         BIGSERIAL   NOT NULL,
    patient_id BIGINT      NOT NULL,
    aptt_value NUMERIC     NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    deleted_at TIMESTAMPTZ,
    CONSTRAINT pk_aptt_values__id PRIMARY KEY (id),
    CONSTRAINT fk_aptt_values__patients__patient_id FOREIGN KEY (patient_id) REFERENCES patients_heparin (id) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE heparin_dosages
(
    id                BIGSERIAL   NOT NULL,
    patient_id        BIGINT      NOT NULL,
    dosage_continuous NUMERIC     NOT NULL,
    dosage_bolus      NUMERIC     NOT NULL,
    created_at        TIMESTAMPTZ NOT NULL,
    updated_at        TIMESTAMPTZ NOT NULL,
    deleted_at        TIMESTAMPTZ,
    CONSTRAINT pk_heparin_dosages__id PRIMARY KEY (id),
    CONSTRAINT fk_heparin_dosages__patients__patient_id FOREIGN KEY (patient_id) REFERENCES patients_heparin (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TRIGGER trg_patients_heparin_set_created_at
    BEFORE INSERT
    ON patients_heparin
    FOR EACH ROW
EXECUTE PROCEDURE set_created_at();

CREATE TRIGGER trg_aptt_values_set_created_at
    BEFORE INSERT
    ON aptt_values
    FOR EACH ROW
EXECUTE PROCEDURE set_created_at();

CREATE TRIGGER trg_heparin_dosages_set_created_at
    BEFORE INSERT
    ON aptt_values
    FOR EACH ROW
EXECUTE PROCEDURE set_created_at();


CREATE TRIGGER trg_patients_heparin_set_updated_at
    BEFORE INSERT
    ON patients_heparin
    FOR EACH ROW
EXECUTE PROCEDURE set_updated_at();

CREATE TRIGGER trg_aptt_values_set_updated_at
    BEFORE INSERT
    ON aptt_values
    FOR EACH ROW
EXECUTE PROCEDURE set_updated_at();

CREATE TRIGGER trg_heparin_dosages_set_updated_at
    BEFORE INSERT
    ON aptt_values
    FOR EACH ROW
EXECUTE PROCEDURE set_updated_at();