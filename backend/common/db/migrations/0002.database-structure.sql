--
-- file: breviary/backend/common/db/migrations/0002.database-structure.sql
-- depends: 0001.initial-schema
--

CREATE TYPE SEX AS ENUM (
    'M',
    'F'
    );

CREATE TABLE patients
(
    id                  BIGSERIAL   NOT NULL,
    first_name          TEXT,
    last_name           TEXT,
    date_of_birth       date,
    height              NUMERIC,
    weight              NUMERIC,              --NOT NULL if heparin=TRUE
    sex                 SEX,
    active              BOOLEAN     NOT NULL, -- default false, false means the patient is in IKEM DB but not in app DB
    heparin             BOOLEAN     NOT NULL, -- true if patient in heparin part of app
    insulin             BOOLEAN     NOT NULL, -- true if patient in insulin part of app
    target_aptt_low     NUMERIC,              --NOT NULL if heparin=TRUE
    target_aptt_high    NUMERIC,              --NOT NULL if heparin=TRUE
    solution_heparin_iu NUMERIC,              --NOT NULL if heparin=TRUE
    solution_ml         NUMERIC,              --NOT NULL if heparin=TRUE
    tddi                NUMERIC,              -- NOT NULL if insulin=TRUE; total daily dose of insulin
    target_glycemia     NUMERIC,              -- NOT NULL if insulin=TRUE
    other_params        jsonb,
    created_at          TIMESTAMPTZ NOT NULL,
    updated_at          TIMESTAMPTZ NOT NULL,
    deleted_at          TIMESTAMPTZ,
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
    CONSTRAINT fk_aptt_values__patients__patient_id FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE heparin_dosages
(
    id                        BIGSERIAL   NOT NULL,
    patient_id                BIGINT      NOT NULL,
    dosage_heparin_continuous NUMERIC     NOT NULL,
    dosage_heparin_bolus      NUMERIC     NOT NULL,
    created_at                TIMESTAMPTZ NOT NULL,
    updated_at                TIMESTAMPTZ NOT NULL,
    deleted_at                TIMESTAMPTZ,
    CONSTRAINT pk_heparin_dosages__id PRIMARY KEY (id),
    CONSTRAINT fk_heparin_dosages__patients__patient_id FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE glycemia_values
(
    id             BIGSERIAL   NOT NULL,
    patient_id     BIGINT      NOT NULL,
    glycemia_value NUMERIC     NOT NULL,
    created_at     TIMESTAMPTZ NOT NULL,
    updated_at     TIMESTAMPTZ NOT NULL,
    deleted_at     TIMESTAMPTZ,
    CONSTRAINT pk_glycemia_values__id PRIMARY KEY (id),
    CONSTRAINT fk_glycemia_values__patients__patient_id FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE carbohydrate_intake_values
(
    id                        BIGSERIAL   NOT NULL,
    patient_id                BIGINT      NOT NULL,
    carbohydrate_intake_value NUMERIC     NOT NULL,
    created_at                TIMESTAMPTZ NOT NULL,
    updated_at                TIMESTAMPTZ NOT NULL,
    deleted_at                TIMESTAMPTZ,
    CONSTRAINT pk_carbohydrate_intake_values__id PRIMARY KEY (id),
    CONSTRAINT fk_carbohydrate_intake_values__patients__patient_id FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE insulin_dosages
(
    id             BIGSERIAL   NOT NULL,
    patient_id     BIGINT      NOT NULL,
    dosage_insulin NUMERIC     NOT NULL,
    created_at     TIMESTAMPTZ NOT NULL,
    updated_at     TIMESTAMPTZ NOT NULL,
    deleted_at     TIMESTAMPTZ,
    CONSTRAINT pk_insulin_dosages__id PRIMARY KEY (id),
    CONSTRAINT fk_insulin_dosages__patients__patient_id FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TRIGGER trg_patients_heparin_set_created_at
    BEFORE INSERT
    ON patients
    FOR EACH ROW
EXECUTE PROCEDURE set_created_at();

CREATE TRIGGER trg_aptt_values_set_created_at
    BEFORE INSERT
    ON aptt_values
    FOR EACH ROW
EXECUTE PROCEDURE set_created_at();

CREATE TRIGGER trg_heparin_dosages_set_created_at
    BEFORE INSERT
    ON heparin_dosages
    FOR EACH ROW
EXECUTE PROCEDURE set_created_at();

CREATE TRIGGER trg_glycemia_values_set_created_at
    BEFORE INSERT
    ON glycemia_values
    FOR EACH ROW
EXECUTE PROCEDURE set_created_at();

CREATE TRIGGER trg_carbohydrate_intake_values_set_created_at
    BEFORE INSERT
    ON carbohydrate_intake_values
    FOR EACH ROW
EXECUTE PROCEDURE set_created_at();


CREATE TRIGGER trg_insulin_dosages_set_created_at
    BEFORE INSERT
    ON insulin_dosages
    FOR EACH ROW
EXECUTE PROCEDURE set_created_at();



CREATE TRIGGER trg_patients_heparin_set_updated_at
    BEFORE INSERT
    ON patients
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

CREATE TRIGGER trg_glycemia_values_set_updated_at
    BEFORE INSERT
    ON glycemia_values
    FOR EACH ROW
EXECUTE PROCEDURE set_updated_at();

CREATE TRIGGER trg_carbohydrate_intake_values_set_updated_at
    BEFORE INSERT
    ON carbohydrate_intake_values
    FOR EACH ROW
EXECUTE PROCEDURE set_updated_at();


CREATE TRIGGER trg_insulin_dosages_set_updated_at
    BEFORE INSERT
    ON insulin_dosages
    FOR EACH ROW
EXECUTE PROCEDURE set_updated_at();
