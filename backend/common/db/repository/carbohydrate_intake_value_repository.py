from typing import List, Optional, cast

from sqlalchemy import desc
from sqlalchemy.orm import Session  # pylint: disable=import-error

from backend.common.db.database import get_db_session
from backend.common.db.model.carbohydrate_intake_value import CarbohydrateIntakeValue
from backend.common.db.repository.base_repository import BaseRepository


class CarbohydrateIntakeValueRepository(BaseRepository):
    """
    CarbohydrateIntakeValue repository
    """

    @staticmethod
    def get_all() -> List[CarbohydrateIntakeValue]:
        sup = super(CarbohydrateIntakeValueRepository, CarbohydrateIntakeValueRepository)
        return sup.base_get_all(CarbohydrateIntakeValue)  # type: ignore

    @staticmethod
    def create(carbohydrate_intake_value: CarbohydrateIntakeValue, commit: bool = True) -> CarbohydrateIntakeValue:
        sup = super(CarbohydrateIntakeValueRepository, CarbohydrateIntakeValueRepository)
        return sup.base_create(carbohydrate_intake_value, commit)  # type: ignore

    @staticmethod
    def create_many(carbohydrate_intake_values: List[CarbohydrateIntakeValue], commit: bool = True) -> List[
        CarbohydrateIntakeValue]:
        sup = super(CarbohydrateIntakeValueRepository, CarbohydrateIntakeValueRepository)
        sup.base_create_many(carbohydrate_intake_values, commit)  # type: ignore
        return carbohydrate_intake_values

    @staticmethod
    def count(session: Optional[Session] = None) -> int:
        session = session if session else get_db_session()
        assert session is not None, "DB must be initialized at this point."
        return session.query(CarbohydrateIntakeValue).count()  # type: ignore  # pylint: disable=no-member

    @staticmethod
    def get_by_id(idd: int) -> Optional[CarbohydrateIntakeValue]:
        sup = super(CarbohydrateIntakeValueRepository, CarbohydrateIntakeValueRepository)
        return sup.base_get_by_id(CarbohydrateIntakeValue, idd)  # type: ignore

    @staticmethod
    def get_by_patient_id(patient_id: int) -> List[CarbohydrateIntakeValue]:
        session = BaseRepository.get_session()
        # pylint: disable=E1101,C0301
        item = session.query(CarbohydrateIntakeValue).filter(CarbohydrateIntakeValue.patient_id == patient_id) \
            .order_by(desc(CarbohydrateIntakeValue.id)).all()  # type: ignore  # noqa: E501
        return cast(List[CarbohydrateIntakeValue], item)
