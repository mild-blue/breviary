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

INSERT INTO patients (id, first_name, last_name, date_of_birth, height, weight, sex, active, heparin, insulin,
                      target_aptt_low, target_aptt_high, solution_heparin_iu, solution_ml, tddi, target_glycemia,
                      other_params)

VALUES (3,
        'Anna',
        'Novakova',
        '1980-11-20 18:00:00.000000',
        180,
        89,
        'F',
        FALSE,
        TRUE,
        FALSE,
        1.5,
        2.3,
        25000,
        500,
        50,
        6.5,
        '{}');


INSERT INTO patients (id, first_name, last_name, date_of_birth, height, weight, sex, active, heparin, insulin,
                      target_aptt_low, target_aptt_high, solution_heparin_iu, solution_ml, tddi, target_glycemia,
                      other_params)

VALUES (4,
        'Frantisek',
        'Dobrota',
        '1980-11-20 18:00:00.000000',
        180,
        89,
        'M',
        FALSE,
        TRUE,
        FALSE,
        1.5,
        2.3,
        25000,
        500,
        50.7,
        7.2,
        '{}');

INSERT INTO patients (id, first_name, last_name, date_of_birth, height, weight, sex, active, heparin, insulin,
                      target_aptt_low, target_aptt_high, solution_heparin_iu, solution_ml, tddi, target_glycemia,
                      other_params)

VALUES (5, 'John', 'Doe', '1950-11-20 18:00:00.000000', 180, 89, 'M', FALSE, FALSE, FALSE, NULL, NULL, NULL, NULL, NULL,
        NULL, '{}'),
       (6, 'Jan', 'Bily', '1956-05-13 18:00:00.000000', 178, 84, 'M', FALSE, FALSE, FALSE, NULL, NULL, NULL, NULL, NULL,
        NULL, '{}'),
       (7, 'Karolina', 'Valkova', '1961-02-11 18:00:00.000000', 165, 77, 'F', FALSE, FALSE, FALSE, NULL, NULL, NULL, NULL,
        NULL, NULL, '{}'),
       (8, 'Petr', 'Malec', '1955-07-22 18:00:00.000000', 170, 88, 'M', FALSE, FALSE, FALSE, NULL, NULL, NULL, NULL,
        NULL, NULL, '{}'),
       (9, 'Amy', 'Black', '1972-01-14 18:00:00.000000', 171, 85, 'F', FALSE, FALSE, FALSE, NULL, NULL, NULL, NULL,
        NULL, NULL, '{}'),
       (10, 'Gene', 'Hackman', '1948-08-19 18:00:00.000000', 166, 75, 'M', FALSE, FALSE, FALSE, NULL, NULL, NULL, NULL,
        NULL, NULL, '{}'),
       (11, 'Klara', 'Mala', '1968-02-13 18:00:00.000000', 162, 53, 'F', FALSE, FALSE, FALSE, NULL, NULL, NULL, NULL,
        NULL, NULL, '{}'),
       (12, 'Jana', 'Stara', '1933-10-01 18:00:00.000000', 171, 92, 'F', FALSE, FALSE, FALSE, NULL, NULL, NULL, NULL,
        NULL, NULL, '{}'),
       (13, 'Karel', 'Vela', '1961-05-01 18:00:00.000000', 180, 105, 'M', FALSE, FALSE, FALSE, NULL, NULL, NULL, NULL,
        NULL, NULL, '{}'),
       (14, 'Filip', 'Machala', '1954-03-04 18:00:00.000000', 188, 113, 'M', FALSE, FALSE, FALSE, NULL, NULL, NULL,
        NULL, NULL, NULL, '{}'),
       (15, 'Ctibor', 'Nerad', '1955-04-01 18:00:00.000000', 174, 99, 'M', FALSE, FALSE, FALSE, NULL, NULL, NULL, NULL,
        NULL, NULL, '{}');


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


---

SELECT setval('app_users_id_seq', COALESCE((SELECT MAX(id)+1 FROM app_users), 1), false);
SELECT setval('aptt_values_id_seq', COALESCE((SELECT MAX(id)+1 FROM aptt_values), 1), false);
SELECT setval('carbohydrate_intake_values_id_seq', COALESCE((SELECT MAX(id)+1 FROM carbohydrate_intake_values), 1), false);
SELECT setval('glycemia_values_id_seq', COALESCE((SELECT MAX(id)+1 FROM glycemia_values), 1), false);
SELECT setval('heparin_dosages_id_seq', COALESCE((SELECT MAX(id)+1 FROM heparin_dosages), 1), false);
SELECT setval('insulin_dosages_id_seq', COALESCE((SELECT MAX(id)+1 FROM insulin_dosages), 1), false);
SELECT setval('patients_id_seq', COALESCE((SELECT MAX(id)+1 FROM patients), 1), false);
