from typing import List, Optional, cast

from sqlalchemy import desc
from sqlalchemy.orm import Session  # pylint: disable=import-error

from backend.common.db.database import get_db_session
from backend.common.db.model.glycemia_value import GlycemiaValue
from backend.common.db.repository.base_repository import BaseRepository


class GlycemiaValueRepository(BaseRepository):
    """
    GlycemiaValue repository
    """

    @staticmethod
    def get_all() -> List[GlycemiaValue]:
        sup = super(GlycemiaValueRepository, GlycemiaValueRepository)
        return sup.base_get_all(GlycemiaValue)  # type: ignore

    @staticmethod
    def create(glycemia_value: GlycemiaValue, commit: bool = True) -> GlycemiaValue:
        sup = super(GlycemiaValueRepository, GlycemiaValueRepository)
        return sup.base_create(glycemia_value, commit)  # type: ignore

    @staticmethod
    def create_many(glycemia_values: List[GlycemiaValue], commit: bool = True) -> List[GlycemiaValue]:
        sup = super(GlycemiaValueRepository, GlycemiaValueRepository)
        sup.base_create_many(glycemia_values, commit)  # type: ignore
        return glycemia_values

    @staticmethod
    def count(session: Optional[Session] = None) -> int:
        session = session if session else get_db_session()
        assert session is not None, "DB must be initialized at this point."
        return session.query(GlycemiaValue).count()  # type: ignore  # pylint: disable=no-member

    @staticmethod
    def get_by_id(idd: int) -> Optional[GlycemiaValue]:
        sup = super(GlycemiaValueRepository, GlycemiaValueRepository)
        return sup.base_get_by_id(GlycemiaValue, idd)  # type: ignore

    @staticmethod
    def get_by_patient_id(patient_id: int) -> List[GlycemiaValue]:
        session = BaseRepository.get_session()
        # pylint: disable=E1101,C0301
        item = session.query(GlycemiaValue).filter(GlycemiaValue.patient_id == patient_id) \
            .order_by(desc(GlycemiaValue.id)).all()  # type: ignore  # noqa: E501
        return cast(List[GlycemiaValue], item)
