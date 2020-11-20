--
-- file: breviary/backend/common/db/migrations/0004.data.sql
-- depends: 0003.data
--

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
        25,
        12,
        36,
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
        25,
        12,
        36,
        '{}');
