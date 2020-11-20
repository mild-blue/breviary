import unittest
from datetime import datetime, timedelta

from backend.heparin.heparin_dosage import DEFAULT_WEIGHT_TO_DOSAGE, _linear_interpolation, \
    _default_heparin_continuous_dosage, recommended_heparin, REMAINDER_STANDARD_HOURS, REMAINDER_FIRST_HOURS


class TestHeparinDosage(unittest.TestCase):
    def test__linear_interpolation(self):
        for index in range(1, len(DEFAULT_WEIGHT_TO_DOSAGE)):
            self.assertEqual(_linear_interpolation(value=DEFAULT_WEIGHT_TO_DOSAGE[index][0],
                                                   lower_bound=DEFAULT_WEIGHT_TO_DOSAGE[index - 1],
                                                   upper_bound=DEFAULT_WEIGHT_TO_DOSAGE[index]),
                             DEFAULT_WEIGHT_TO_DOSAGE[index][1])

    def test__default_dosage(self):
        expected_weight_to_dosage = [
            (51, 18.5),
            (53, 19),
            (55, 19.5),
            (63, 22.5),
            (65, 23.5),
            (67, 24),
            (101, 36),
            (100, 36),
            (1000, 36),
            (50, 18),
            (49, 18),
            (4, 18)
        ]
        for expected_dosage in expected_weight_to_dosage:
            self.assertEqual(_default_heparin_continuous_dosage(expected_dosage[0]), expected_dosage[1])

    def test_recommended_heparin(self):
        data_inputs = [
            (83, 1.5, 2, 1.8, None, 25000, 500, 20, None),
            (83, 1.5, 2, None, None, 25000, 500, None, None)
        ]
        expected_outputs = [
            (20, 0, REMAINDER_STANDARD_HOURS, None),
            (30.0, 0, REMAINDER_FIRST_HOURS, None)
        ]

        for index in range(0, len(data_inputs) - 1):
            data_input = data_inputs[index]
            expected_output = expected_outputs[index]
            reco = recommended_heparin(data_input[0], data_input[1], data_input[2], data_input[3], data_input[4],
                                       data_input[5], data_input[6], data_input[7], data_input[8])
            self.assertEqual(expected_output[0], reco.heparin_continuous_dosage)
            self.assertEqual(expected_output[1], reco.heparin_bolus_dosage)
            self.assertLess(datetime.now() + timedelta(hours=expected_output[2], minutes=-1), reco.next_remainder)
            self.assertGreater(datetime.now() + timedelta(hours=expected_output[2], minutes=1), reco.next_remainder)
            self.assertEqual(expected_output[3], reco.doctor_warning)
