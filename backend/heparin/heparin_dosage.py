from dataclasses import dataclass
from datetime import datetime


@dataclass
class HeparinRecommendation:
    heparin_continuous_dosage: float
    heparin_bolus_dosage: float
    next_remainder: datetime
    doctor_warning: str = None


def recommended_heparin(
        weight: float,
        target_aptt_low: float,
        target_aptt_high: float,
        current_aptt: float,
        previous_aptt: float,
        solution_heparin_units: float,
        solution_ml: float
) -> HeparinRecommendation:
    return 0


def _calculate_recommended_dosage(
        weight: float,
        target_aptt_low: float,
        target_aptt_high: float,
        current_aptt: float,
        solution_heparin_units: float,
        solution_ml: float
) -> float:
    return 0
