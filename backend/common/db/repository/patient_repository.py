from typing import List, Optional

from sqlalchemy.orm import Session  # pylint: disable=import-error

from backend.common.db.database import get_db_session
from backend.common.db.model.patient import Patient
from backend.common.db.repository.base_repository import BaseRepository


class PatientRepository(BaseRepository):
    """
    Patient repository
    """

    @staticmethod
    def get_all() -> List[Patient]:
        sup = super(PatientRepository, PatientRepository)
        return sup.base_get_all(Patient)  # type: ignore

    @staticmethod
    def create(patient: Patient, commit: bool = True) -> Patient:
        sup = super(PatientRepository, PatientRepository)
        return sup.base_create(patient, commit)  # type: ignore

    @staticmethod
    def create_many(patients: List[Patient], commit: bool = True) -> List[Patient]:
        sup = super(PatientRepository, PatientRepository)
        sup.base_create_many(patients, commit)  # type: ignore
        return patients

    @staticmethod
    def count(session: Optional[Session] = None) -> int:
        session = session if session else get_db_session()
        assert session is not None, "DB must be initialized at this point."
        return session.query(Patient).count()  # type: ignore  # pylint: disable=no-member

    @staticmethod
    def get_by_id(idd: int) -> Optional[Patient]:
        sup = super(PatientRepository, PatientRepository)
        return sup.base_get_by_id(Patient, idd)  # type: ignore
