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
        500,
        55,
        6,
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
        500,
        52,
        7,
        '{}');

---

INSERT INTO aptt_values (id, patient_id, aptt_value)
VALUES (1, 1, 1.2);
INSERT INTO aptt_values (id, patient_id, aptt_value)
VALUES (2, 1, 2.2);
INSERT INTO aptt_values (id, patient_id, aptt_value)
VALUES (3, 1, 2.8);

INSERT INTO aptt_values (id, patient_id, aptt_value)
VALUES (4, 2, 3.5);
INSERT INTO aptt_values (id, patient_id, aptt_value)
VALUES (5, 2, 2.01);
INSERT INTO aptt_values (id, patient_id, aptt_value)
VALUES (6, 2, 1.7);

---

INSERT INTO carbohydrate_intake_values (id, patient_id, carbohydrate_intake_value)
VALUES (1, 1, 70);
INSERT INTO carbohydrate_intake_values (id, patient_id, carbohydrate_intake_value)
VALUES (2, 1, 40);
INSERT INTO carbohydrate_intake_values (id, patient_id, carbohydrate_intake_value)
VALUES (3, 1, 85);

INSERT INTO carbohydrate_intake_values (id, patient_id, carbohydrate_intake_value)
VALUES (4, 2, 50);
INSERT INTO carbohydrate_intake_values (id, patient_id, carbohydrate_intake_value)
VALUES (5, 2, 55);
INSERT INTO carbohydrate_intake_values (id, patient_id, carbohydrate_intake_value)
VALUES (6, 2, 66);

---

INSERT INTO glycemia_values (id, patient_id, glycemia_value)
VALUES (1, 1, 10);
INSERT INTO glycemia_values (id, patient_id, glycemia_value)
VALUES (2, 1, 12);
INSERT INTO glycemia_values (id, patient_id, glycemia_value)
VALUES (3, 1, 8);

INSERT INTO glycemia_values (id, patient_id, glycemia_value)
VALUES (4, 2, 9);
INSERT INTO glycemia_values (id, patient_id, glycemia_value)
VALUES (5, 2, 9.5);
INSERT INTO glycemia_values (id, patient_id, glycemia_value)
VALUES (6, 2, 9.7);

---

INSERT INTO heparin_dosages (id, patient_id, dosage_heparin_continuous, dosage_heparin_bolus)
VALUES (1, 1, 19, 0);
INSERT INTO heparin_dosages (id, patient_id, dosage_heparin_continuous, dosage_heparin_bolus)
VALUES (2, 1, 22, 80);
INSERT INTO heparin_dosages (id, patient_id, dosage_heparin_continuous, dosage_heparin_bolus)
VALUES (3, 1, 23.2, 35);

INSERT INTO heparin_dosages (id, patient_id, dosage_heparin_continuous, dosage_heparin_bolus)
VALUES (4, 2, 18.1, 0);
INSERT INTO heparin_dosages (id, patient_id, dosage_heparin_continuous, dosage_heparin_bolus)
VALUES (5, 2, 19, 0);
INSERT INTO heparin_dosages (id, patient_id, dosage_heparin_continuous, dosage_heparin_bolus)
VALUES (6, 2, 20.1, 60);

---

INSERT INTO insulin_dosages (id, patient_id, dosage_insulin)
VALUES (1, 1, 10.9);
INSERT INTO insulin_dosages (id, patient_id, dosage_insulin)
VALUES (2, 1, 9.8);
INSERT INTO insulin_dosages (id, patient_id, dosage_insulin)
VALUES (3, 1, 8.7);

INSERT INTO insulin_dosages (id, patient_id, dosage_insulin)
VALUES (4, 2, 12.3);
INSERT INTO insulin_dosages (id, patient_id, dosage_insulin)
VALUES (5, 2, 6.1);
INSERT INTO insulin_dosages (id, patient_id, dosage_insulin)
VALUES (6, 2, 7.1);
