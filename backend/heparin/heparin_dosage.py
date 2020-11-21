from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Tuple, Optional


@dataclass
class HeparinRecommendation:
    heparin_continuous_dosage: float
    heparin_bolus_dosage: float
    next_remainder: datetime
    doctor_warning: str = None


LOWEST_APTT = 1.2
LOW_APTT = 1.5
STANDARD_APTT = 2.3
HIGH_APTT = 3
HIGHEST_APTT = 3.5

LOWEST_APTT_DOSAGE_PER_KG_CHANGE = 4
LOW_APTT_DOSAGE_PER_KG_CHANGE = 2
BELOW_STANDARD_APTT_DOSAGE_PER_KG_CHANGE = 1
ABOVE_STANDARD_APTT_DOSAGE_PER_KG_CHANGE = -1
HIGH_APTT_DOSAGE_PER_KG_CHANGE = -2
HIGHEST_APTT_DOSAGE_PER_KG_CHANGE = -3

LOWEST_APTT_BOLUS = 80
LOW_APTT_BOLUS = 40

REMAINDER_STANDARD_HOURS = 6
REMAINDER_FIRST_HOURS = 4
REMAINDER_NONCOAGULATING_HOURS = 1

EXTREME_DOSAGE_DIFF = 15

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


def _linear_interpolation(value: float, lower_bound: Tuple[float], upper_bound: Tuple[float]) -> float:
    a = (upper_bound[1] - lower_bound[1]) / (upper_bound[0] - lower_bound[0])
    b = lower_bound[1] - a * lower_bound[0]
    return a * value + b


def _default_heparin_continuous_dosage(patient_weight: float) -> float:
    if patient_weight <= DEFAULT_WEIGHT_TO_DOSAGE[0][0]:
        return DEFAULT_WEIGHT_TO_DOSAGE[0][1]
    if patient_weight >= DEFAULT_WEIGHT_TO_DOSAGE[-1][0]:
        return DEFAULT_WEIGHT_TO_DOSAGE[-1][1]

    for index in range(0, len(DEFAULT_WEIGHT_TO_DOSAGE)):
        if patient_weight <= DEFAULT_WEIGHT_TO_DOSAGE[index][0]:
            return _linear_interpolation(patient_weight, DEFAULT_WEIGHT_TO_DOSAGE[index - 1],
                                         DEFAULT_WEIGHT_TO_DOSAGE[index])
    raise AssertionError("Value should be always returned. Some issue with the code")


def _get_new_dosage(current_dosage: float, weight: float, units_per_kg: float, solution_heparin_units: float,
                    solution_ml: float) -> float:
    return current_dosage + units_per_kg * weight * solution_ml / solution_heparin_units


def _calculate_bolus(weight: float, solution_heparin_units: float, solution_ml: float, units_per_kg: float) -> float:
    return units_per_kg * weight * solution_ml / solution_heparin_units


def _calculate_recommended_dosage(weight: float,
                                  target_aptt_low: float,
                                  target_aptt_high: float,
                                  current_aptt: Optional[float],
                                  solution_heparin_units: float,
                                  solution_ml: float,
                                  current_continuous_dosage: Optional[float],
                                  previous_continuous_dosage: Optional[float]) -> \
        (float, float):  # (continuous_dosage, bolus)
    if current_aptt is None:  # initial setup, no measurements yet
        return _default_heparin_continuous_dosage(weight), 0
    elif current_continuous_dosage == 0:
        return _get_new_dosage(previous_continuous_dosage, weight, HIGHEST_APTT_DOSAGE_PER_KG_CHANGE,
                               solution_heparin_units, solution_ml), 0
    elif current_aptt < LOWEST_APTT:
        return _get_new_dosage(current_continuous_dosage, weight, LOWEST_APTT_DOSAGE_PER_KG_CHANGE,
                               solution_heparin_units, solution_ml), \
               _calculate_bolus(weight, solution_heparin_units, solution_ml, LOWEST_APTT_BOLUS)
    elif current_aptt < LOW_APTT:
        return _get_new_dosage(current_continuous_dosage, weight, LOW_APTT_DOSAGE_PER_KG_CHANGE, solution_heparin_units,
                               solution_ml), \
               _calculate_bolus(weight, solution_heparin_units, solution_ml, LOW_APTT_BOLUS)
    elif current_aptt < target_aptt_low:
        return _get_new_dosage(current_continuous_dosage, weight, BELOW_STANDARD_APTT_DOSAGE_PER_KG_CHANGE,
                               solution_heparin_units, solution_ml), 0
    elif current_aptt < target_aptt_high:
        return current_continuous_dosage, 0
    elif current_aptt < STANDARD_APTT:
        return _get_new_dosage(current_continuous_dosage, weight, ABOVE_STANDARD_APTT_DOSAGE_PER_KG_CHANGE,
                               solution_heparin_units, solution_ml), 0
    elif current_aptt < HIGH_APTT:
        return _get_new_dosage(current_continuous_dosage, weight, HIGH_APTT_DOSAGE_PER_KG_CHANGE,
                               solution_heparin_units, solution_ml), 0
    else:
        return 0, 0


def _get_next_remainder(current_aptt: float, heparin_continuous_dosage: float) -> datetime:
    if current_aptt is None:  # initial setup, measure after 4 hours
        return datetime.now() + timedelta(hours=REMAINDER_FIRST_HOURS)
    elif heparin_continuous_dosage == 0:  # stop heparin for one hour
        return datetime.now() + timedelta(hours=REMAINDER_NONCOAGULATING_HOURS)
    else:
        return datetime.now() + timedelta(hours=REMAINDER_STANDARD_HOURS)


def _get_doctor_warning(current_aptt: float, previous_aptt: float, heparin_continuous_dosage: float,
                        weight: float) -> Optional[str]:
    if current_aptt is None or previous_aptt is None or heparin_continuous_dosage is None:
        return None
    elif current_aptt < LOWEST_APTT > previous_aptt:
        return f"aPTT below {LOWEST_APTT} for 2 consecutive measurements."
    elif current_aptt > HIGHEST_APTT < previous_aptt:
        return f"aPTT above {HIGHEST_APTT} for 2 consecutive measurements."
    elif abs(heparin_continuous_dosage - _default_heparin_continuous_dosage(weight)) >= EXTREME_DOSAGE_DIFF:
        return f"Current continuous heparin dosage differs from default weight based dosage by " \
               f"{abs(heparin_continuous_dosage - _default_heparin_continuous_dosage(weight))}"
    else:
        return None


def recommended_heparin(weight: float,
                        target_aptt_low: float,
                        target_aptt_high: float,
                        current_aptt: Optional[float],
                        previous_aptt: Optional[float],
                        solution_heparin_units: float,
                        solution_ml: float,
                        current_continuous_dosage: Optional[float],
                        previous_continuous_dosage: Optional[float]) \
        -> HeparinRecommendation:
    heparin_continuous_dosage, heparin_bolus_dosage = _calculate_recommended_dosage(weight,
                                                                                    target_aptt_low,
                                                                                    target_aptt_high,
                                                                                    current_aptt,
                                                                                    solution_heparin_units,
                                                                                    solution_ml,
                                                                                    current_continuous_dosage,
                                                                                    previous_continuous_dosage)
    next_remainder = _get_next_remainder(current_aptt, heparin_continuous_dosage)
    doctor_warning = _get_doctor_warning(current_aptt, previous_aptt, heparin_continuous_dosage, weight)
    return HeparinRecommendation(heparin_continuous_dosage, heparin_bolus_dosage, next_remainder, doctor_warning)


if __name__ == '__main__':
    reco = recommended_heparin(99, 1.5, 2, 2.8, 3.2, 25000, 500, 16, 20)
    print(reco.heparin_continuous_dosage, reco.heparin_bolus_dosage, reco.next_remainder, reco.doctor_warning)
