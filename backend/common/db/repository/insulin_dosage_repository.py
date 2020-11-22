from typing import List, Optional, cast

from sqlalchemy import desc
from sqlalchemy.orm import Session  # pylint: disable=import-error

from backend.common.db.database import get_db_session
from backend.common.db.model.insulin_dosage import InsulinDosage
from backend.common.db.repository.base_repository import BaseRepository


class InsulinDosageRepository(BaseRepository):
    """
    InsulinDosage repository
    """

    @staticmethod
    def get_all() -> List[InsulinDosage]:
        sup = super(InsulinDosageRepository, InsulinDosageRepository)
        return sup.base_get_all(InsulinDosage)  # type: ignore

    @staticmethod
    def create(insulin_dosage: InsulinDosage, commit: bool = True) -> InsulinDosage:
        sup = super(InsulinDosageRepository, InsulinDosageRepository)
        return sup.base_create(insulin_dosage, commit)  # type: ignore

    @staticmethod
    def create_many(insulin_dosages: List[InsulinDosage], commit: bool = True) -> List[InsulinDosage]:
        sup = super(InsulinDosageRepository, InsulinDosageRepository)
        sup.base_create_many(insulin_dosages, commit)  # type: ignore
        return insulin_dosages

    @staticmethod
    def count(session: Optional[Session] = None) -> int:
        session = session if session else get_db_session()
        assert session is not None, "DB must be initialized at this point."
        return session.query(InsulinDosage).count()  # type: ignore  # pylint: disable=no-member

    @staticmethod
    def get_by_id(idd: int) -> Optional[InsulinDosage]:
        sup = super(InsulinDosageRepository, InsulinDosageRepository)
        return sup.base_get_by_id(InsulinDosage, idd)  # type: ignore

    @staticmethod
    def get_by_patient_id(patient_id: int) -> List[InsulinDosage]:
        session = BaseRepository.get_session()
        # pylint: disable=E1101,C0301
        item = session.query(InsulinDosage).filter(InsulinDosage.patient_id == patient_id) \
            .order_by(desc(InsulinDosage.id)).all()  # type: ignore  # noqa: E501
        return cast(List[InsulinDosage], item)
