import unittest

from backend.insulin.insulin_dosage import recommended_insulin


class TestInsulinDosage(unittest.TestCase):

    def test_recommended_insulin(self):
        data_inputs = [
            (50, 8, 10, 70),
            (50, 8, 5, 70),
            (30, 8, 5, 70)
        ]
        expected_outputs = [
            10.909090909090908,
            8.636363636363637,
            5.181818181818182
        ]
        for index in range(0, len(data_inputs)):
            data_input = data_inputs[index]
            expected_output = expected_outputs[index]
            self.assertEqual(expected_output,
                             recommended_insulin(data_input[0], data_input[1], data_input[2], data_input[3]))
