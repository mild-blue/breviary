--
-- file: breviary/backend/common/db/migrations/0006.set_index_values.sql
-- depends: 0005.data5
--

SELECT pg_catalog.setval('public.app_users_id_seq', 1, true);
SELECT pg_catalog.setval('public.aptt_values_id_seq', 6, true);
SELECT pg_catalog.setval('public.carbohydrate_intake_values_id_seq', 6, true);
SELECT pg_catalog.setval('public.glycemia_values_id_seq', 6, true);
SELECT pg_catalog.setval('public.heparin_dosages_id_seq', 6, true);
SELECT pg_catalog.setval('public.insulin_dosages_id_seq', 6, true);
SELECT pg_catalog.setval('public.patients_id_seq', 15, true);