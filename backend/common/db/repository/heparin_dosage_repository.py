from typing import List, Optional, cast

from sqlalchemy import desc
from sqlalchemy.orm import Session  # pylint: disable=import-error

from backend.common.db.database import get_db_session
from backend.common.db.model.heparin_dosage import HeparinDosage
from backend.common.db.repository.base_repository import BaseRepository


class HeparinDosageRepository(BaseRepository):
    """
    HeparinDosage repository
    """

    @staticmethod
    def get_all() -> List[HeparinDosage]:
        sup = super(HeparinDosageRepository, HeparinDosageRepository)
        return sup.base_get_all(HeparinDosage)  # type: ignore

    @staticmethod
    def create(heparin_dosage: HeparinDosage, commit: bool = True) -> HeparinDosage:
        sup = super(HeparinDosageRepository, HeparinDosageRepository)
        return sup.base_create(heparin_dosage, commit)  # type: ignore

    @staticmethod
    def create_many(heparin_dosages: List[HeparinDosage], commit: bool = True) -> List[HeparinDosage]:
        sup = super(HeparinDosageRepository, HeparinDosageRepository)
        sup.base_create_many(heparin_dosages, commit)  # type: ignore
        return heparin_dosages

    @staticmethod
    def count(session: Optional[Session] = None) -> int:
        session = session if session else get_db_session()
        assert session is not None, "DB must be initialized at this point."
        return session.query(HeparinDosage).count()  # type: ignore  # pylint: disable=no-member

    @staticmethod
    def get_by_id(idd: int) -> Optional[HeparinDosage]:
        sup = super(HeparinDosageRepository, HeparinDosageRepository)
        return sup.base_get_by_id(HeparinDosage, idd)  # type: ignore

    @staticmethod
    def get_newest_by_patient_id(patient_id: int) -> Optional[HeparinDosage]:
        session = BaseRepository.get_session()
        # pylint: disable=E1101,C0301
        item = session.query(HeparinDosage).filter(HeparinDosage.patient_id == patient_id) \
            .order_by(desc(HeparinDosage.id)).first()  # type: ignore  # noqa: E501
        return cast(HeparinDosage, item)

    @staticmethod
    def get_second_newest_by_patient_id(patient_id: int) -> Optional[HeparinDosage]:
        session = BaseRepository.get_session()
        # pylint: disable=E1101,C0301
        items = session.query(HeparinDosage).filter(HeparinDosage.patient_id == patient_id) \
            .order_by(desc(HeparinDosage.id)).all()  # type: ignore  # noqa: E501

        if len(items) > 1:
            return cast(HeparinDosage, items[1])
        return None

    @staticmethod
    def get_by_patient_id(patient_id: int) -> List[HeparinDosage]:
        session = BaseRepository.get_session()
        # pylint: disable=E1101,C0301
        item = session.query(HeparinDosage).filter(HeparinDosage.patient_id == patient_id) \
            .order_by(desc(HeparinDosage.id)).all()  # type: ignore  # noqa: E501
        return cast(List[HeparinDosage], item)
