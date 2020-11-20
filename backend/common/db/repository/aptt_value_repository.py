from typing import List, Optional

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
    def create(app_user: ApttValue, commit: bool = True) -> ApttValue:
        sup = super(ApttValueRepository, ApttValueRepository)
        return sup.base_create(app_user, commit)  # type: ignore

    @staticmethod
    def create_many(app_users: List[ApttValue], commit: bool = True) -> List[ApttValue]:
        sup = super(ApttValueRepository, ApttValueRepository)
        sup.base_create_many(app_users, commit)  # type: ignore
        return app_users

    @staticmethod
    def count(session: Optional[Session] = None) -> int:
        session = session if session else get_db_session()
        assert session is not None, "DB must be initialized at this point."
        return session.query(ApttValue).count()  # type: ignore  # pylint: disable=no-member

    @staticmethod
    def get_by_id(idd: int) -> Optional[ApttValue]:
        sup = super(ApttValueRepository, ApttValueRepository)
        return sup.base_get_by_id(ApttValue, idd)  # type: ignore
