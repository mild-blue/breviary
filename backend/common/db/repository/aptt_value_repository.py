from typing import List, Optional, cast

from sqlalchemy import desc
from sqlalchemy.orm import Session  # pylint: disable=import-error

from backend.common.db.database import get_db_session
from backend.common.db.model.aptt_values import ApttValue
from backend.common.db.repository.base_repository import BaseRepository


class ApttValueRepository(BaseRepository):
    """
    ApttValue repository
    """

    @staticmethod
    def get_all() -> List[ApttValue]:
        sup = super(ApttValueRepository, ApttValueRepository)
        return sup.base_get_all(ApttValue)  # type: ignore

    @staticmethod
    def create(aptt_value: ApttValue, commit: bool = True) -> ApttValue:
        sup = super(ApttValueRepository, ApttValueRepository)
        return sup.base_create(aptt_value, commit)  # type: ignore

    @staticmethod
    def create_many(aptt_values: List[ApttValue], commit: bool = True) -> List[ApttValue]:
        sup = super(ApttValueRepository, ApttValueRepository)
        sup.base_create_many(aptt_values, commit)  # type: ignore
        return aptt_values

    @staticmethod
    def count(session: Optional[Session] = None) -> int:
        session = session if session else get_db_session()
        assert session is not None, "DB must be initialized at this point."
        return session.query(ApttValue).count()  # type: ignore  # pylint: disable=no-member

    @staticmethod
    def get_by_id(idd: int) -> Optional[ApttValue]:
        sup = super(ApttValueRepository, ApttValueRepository)
        return sup.base_get_by_id(ApttValue, idd)  # type: ignore

    @staticmethod
    def get_newest_by_patient_id(patient_id: int) -> Optional[ApttValue]:
        session = BaseRepository.get_session()
        # pylint: disable=E1101,C0301
        item = session.query(ApttValue).filter(ApttValue.patient_id == patient_id) \
            .order_by(desc(ApttValue.id)).first()  # type: ignore  # noqa: E501
        return cast(ApttValue, item)

    @staticmethod
    def get_second_newest_by_patient_id(patient_id: int) -> Optional[ApttValue]:
        session = BaseRepository.get_session()
        # pylint: disable=E1101,C0301
        items = session.query(ApttValue).filter(ApttValue.patient_id == patient_id) \
            .order_by(desc(ApttValue.id)).all()  # type: ignore  # noqa: E501
        
        if len(items) > 1:
            return cast(ApttValue, items[1])
        return None

    @staticmethod
    def get_by_patient_id(patient_id: int) -> List[ApttValue]:
        session = BaseRepository.get_session()
        # pylint: disable=E1101,C0301
        item = session.query(ApttValue).filter(ApttValue.patient_id == patient_id) \
            .order_by(desc(ApttValue.id)).all()  # type: ignore  # noqa: E501
        return cast(List[ApttValue], item)