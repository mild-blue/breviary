--
-- file: breviary/backend/common/db/migrations/0005.data5.sql
-- depends: 0004.data
--

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
