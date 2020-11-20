from typing import List, Optional

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