from dataclasses import dataclass
from datetime import datetime
from typing import List

from backend.common.db.model.enums import Sex, DrugType


@dataclass
class TargetApttDto:
    low: float
    high: float


@dataclass
class PatientDto:
    id: int
    first_name: str
    last_name: str
    date_of_birth: datetime
    height: int
    weight: float
    sex: Sex
    drug_type: DrugType
    target_aptt: TargetApttDto
    actual_aptt: float
    actual_aptt_updated_on: datetime
    actual_dosage: float


@dataclass
class RecommendationDto:
    patient_id: int
    recommended_dosage: float


@dataclass
class DosageDto:
    date: datetime
    value: float


@dataclass
class HistoryEntriesDto:
    dosage_entries: List[DosageDto]
    aptt_entries: List[DosageDto]
