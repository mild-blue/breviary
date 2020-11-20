import unittest

from backend.heparin.heparin_dosage import DEFAULT_WEIGHT_TO_DOSAGE, _linear_interpolation, \
    _default_heparin_continuous_dosage


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
