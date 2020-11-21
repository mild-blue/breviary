import unittest
from datetime import datetime, timedelta

from backend.heparin.heparin_dosage import _linear_interpolation, \
    _default_heparin_continuous_dosage, recommended_heparin, REMAINDER_STANDARD_HOURS, REMAINDER_FIRST_HOURS, \
    LOWEST_APTT, REMAINDER_NONCOAGULATING_HOURS, HIGHEST_APTT

DEFAULT_WEIGHT_TO_DOSAGE = [
    (50, 18),
    (52, 19),
    (54, 19),
    (56, 20),
    (58, 21),
    (60, 22),
    (62, 22),
    (64, 23),
    (66, 24),
    (68, 24),
    (70, 25),
    (72, 26),
    (74, 27),
    (76, 27),
    (78, 28),
    (80, 29),
    (82, 30),
    (84, 30),
    (86, 31),
    (88, 32),
    (90, 32),
    (92, 33),
    (94, 34),
    (96, 35),
    (98, 35),
    (100, 36)
]


class TestHeparinDosage(unittest.TestCase):
    def test__linear_interpolation(self):
        for index in range(1, len(DEFAULT_WEIGHT_TO_DOSAGE)):
            self.assertEqual(_linear_interpolation(value=DEFAULT_WEIGHT_TO_DOSAGE[index][0],
                                                   lower_bound=DEFAULT_WEIGHT_TO_DOSAGE[index - 1],
                                                   upper_bound=DEFAULT_WEIGHT_TO_DOSAGE[index]),
                             DEFAULT_WEIGHT_TO_DOSAGE[index][1])

    def test__default_dosage(self):
        solution_ml = 500
        solution_heparin_units = 25000
        expected_weight_to_dosage = [
            (51, 18.36),
            (53, 19.08),
            (55, 19.8),
            (63, 22.68),
            (65, 23.4),
            (67, 24.12),
            (101, 36),
            (100, 36),
            (1000, 36),
            (50, 18),
            (49, 18),
            (4, 18)
        ]
        for expected_dosage in expected_weight_to_dosage:
            self.assertEqual(
                _default_heparin_continuous_dosage(expected_dosage[0], solution_heparin_units, solution_ml),
                expected_dosage[1])

    def test_recommended_heparin(self):
        data_inputs = [
            (83, 1.5, 2, 1.8, None, 25000, 500, 20, None),
            (83, 1.5, 2, None, None, 25000, 500, None, None),
            (83, 1.5, 2, 1.1, 1.15, 25000, 500, 25, 26),
            (83, 1.5, 2, 3.8, 3.6, 25000, 500, 25, 26),
            (83, 1.5, 2, 2.8, 3.6, 25000, 500, 0, 26),
            (83, 1.5, 2, 2.8, 3.2, 25000, 500, 16, 20),
            (99, 1.5, 2, 2.8, 3.2, 25000, 500, 16, 20)
        ]
        expected_outputs = [
            (20, 0, REMAINDER_STANDARD_HOURS, None),
            (29.88, 0, REMAINDER_FIRST_HOURS, None),
            (31.64, 132.8, REMAINDER_STANDARD_HOURS, f"aPTT below {LOWEST_APTT} for 2 consecutive measurements."),
            (0, 0, REMAINDER_NONCOAGULATING_HOURS, f"aPTT above {HIGHEST_APTT} for 2 consecutive measurements."),
            (21.02, 0, REMAINDER_STANDARD_HOURS, None),
            (12.68, 0, REMAINDER_STANDARD_HOURS,
             "Current continuous heparin dosage differs from default weight based dosage by 17.2"),
            (12.04, 0, REMAINDER_STANDARD_HOURS,
             "Current continuous heparin dosage differs from default weight based dosage by 23.6")

        ]

        for index in range(0, len(data_inputs)):
            data_input = data_inputs[index]
            expected_output = expected_outputs[index]
            reco = recommended_heparin(data_input[0], data_input[1], data_input[2], data_input[3], data_input[4],
                                       data_input[5], data_input[6], data_input[7], data_input[8])
            self.assertEqual(expected_output[0], reco.heparin_continuous_dosage)
            self.assertEqual(expected_output[1], reco.heparin_bolus_dosage)
            self.assertLess(datetime.now() + timedelta(hours=expected_output[2], minutes=-1), reco.next_remainder)
            self.assertGreater(datetime.now() + timedelta(hours=expected_output[2], minutes=1), reco.next_remainder)
            self.assertEqual(expected_output[3], reco.doctor_warning)
