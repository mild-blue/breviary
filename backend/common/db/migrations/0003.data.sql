--
-- file: breviary/backend/common/db/migrations/0003.data.sql
-- depends: 0002.database-structure
--

INSERT INTO patients (id, first_name, last_name, date_of_birth, height, weight, sex, active, heparin, insulin,
                      target_aptt_low, target_aptt_high, solution_heparin_iu, solution_ml, tddi, target_glycemia,
                      other_params)

VALUES (1,
        'Franta',
        'Flinta',
        '1980-11-20 18:00:00.000000',
        180,
        89,
        'M',
        TRUE,
        TRUE,
        FALSE,
        1.5,
        2.3,
        25000,
        25,
        12,
        36,
        '{}');

INSERT INTO patients (id, first_name, last_name, date_of_birth, height, weight, sex, active, heparin, insulin,
                      target_aptt_low, target_aptt_high, solution_heparin_iu, solution_ml, tddi, target_glycemia,
                      other_params)

VALUES (2,
        'Tomas',
        'Novak',
        '1987-10-20 17:00:00.000000',
        180,
        89,
        'M',
        TRUE,
        FALSE,
        TRUE,
        1.5,
        2.3,
        25000,
        25,
        12,
        36,
        '{}');

---

INSERT INTO aptt_values (id, patient_id, aptt_value)
VALUES (1, 1, 111);
INSERT INTO aptt_values (id, patient_id, aptt_value)
VALUES (2, 1, 222);
INSERT INTO aptt_values (id, patient_id, aptt_value)
VALUES (3, 1, 333);

INSERT INTO aptt_values (id, patient_id, aptt_value)
VALUES (4, 2, 444);
INSERT INTO aptt_values (id, patient_id, aptt_value)
VALUES (5, 2, 555);
INSERT INTO aptt_values (id, patient_id, aptt_value)
VALUES (6, 2, 666);

---

INSERT INTO carbohydrate_intake_values (id, patient_id, carbohydrate_intake_value)
VALUES (1, 1, 111);
INSERT INTO carbohydrate_intake_values (id, patient_id, carbohydrate_intake_value)
VALUES (2, 1, 222);
INSERT INTO carbohydrate_intake_values (id, patient_id, carbohydrate_intake_value)
VALUES (3, 1, 333);

INSERT INTO carbohydrate_intake_values (id, patient_id, carbohydrate_intake_value)
VALUES (4, 2, 444);
INSERT INTO carbohydrate_intake_values (id, patient_id, carbohydrate_intake_value)
VALUES (5, 2, 555);
INSERT INTO carbohydrate_intake_values (id, patient_id, carbohydrate_intake_value)
VALUES (6, 2, 666);

---

INSERT INTO glycemia_values (id, patient_id, glycemia_value)
VALUES (1, 1, 111);
INSERT INTO glycemia_values (id, patient_id, glycemia_value)
VALUES (2, 1, 222);
INSERT INTO glycemia_values (id, patient_id, glycemia_value)
VALUES (3, 1, 333);

INSERT INTO glycemia_values (id, patient_id, glycemia_value)
VALUES (4, 2, 444);
INSERT INTO glycemia_values (id, patient_id, glycemia_value)
VALUES (5, 2, 555);
INSERT INTO glycemia_values (id, patient_id, glycemia_value)
VALUES (6, 2, 666);

---

INSERT INTO heparin_dosages (id, patient_id, dosage_heparin_continuous, dosage_heparin_bolus)
VALUES (1, 1, 111, 1111);
INSERT INTO heparin_dosages (id, patient_id, dosage_heparin_continuous, dosage_heparin_bolus)
VALUES (2, 1, 222, 2222);
INSERT INTO heparin_dosages (id, patient_id, dosage_heparin_continuous, dosage_heparin_bolus)
VALUES (3, 1, 333, 3333);

INSERT INTO heparin_dosages (id, patient_id, dosage_heparin_continuous, dosage_heparin_bolus)
VALUES (4, 2, 444, 4444);
INSERT INTO heparin_dosages (id, patient_id, dosage_heparin_continuous, dosage_heparin_bolus)
VALUES (5, 2, 555, 5555);
INSERT INTO heparin_dosages (id, patient_id, dosage_heparin_continuous, dosage_heparin_bolus)
VALUES (6, 2, 666, 6666);

---

INSERT INTO insulin_dosages (id, patient_id, dosage_insulin)
VALUES (1, 1, 111);
INSERT INTO insulin_dosages (id, patient_id, dosage_insulin)
VALUES (2, 1, 222);
INSERT INTO insulin_dosages (id, patient_id, dosage_insulin)
VALUES (3, 1, 333);

INSERT INTO insulin_dosages (id, patient_id, dosage_insulin)
VALUES (4, 2, 444);
INSERT INTO insulin_dosages (id, patient_id, dosage_insulin)
VALUES (5, 2, 555);
INSERT INTO insulin_dosages (id, patient_id, dosage_insulin)
VALUES (6, 2, 666);
