import datetime

from sqlalchemy import Column, Integer, TEXT, Enum, DateTime, func, PrimaryKeyConstraint  # pylint: disable=import-error
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.sql.sqltypes import Boolean

from backend.common.db.base import Base
from backend.common.db.model.enums import Sex
from backend.common.db.model_utils import get_primary_key_name


class Patient(Base):
    """
    Patient class
    """
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = Column(TEXT, unique=True, nullable=True)
    last_name = Column(TEXT, unique=False, nullable=True)
    date_of_birth = Column(DateTime(timezone=True), unique=False, nullable=True)
    height = Column(Integer, unique=False, nullable=True)
    weight = Column(Integer, unique=False, nullable=True)
    sex = Column(Enum(Sex), unique=False, nullable=True)
    active = Column(Boolean, unique=False, nullable=False, default=False)
    heparin = Column(Boolean, unique=False, nullable=False, default=False)
    insulin = Column(Boolean, unique=False, nullable=False, default=False)
    target_aptt_low = Column(Integer, unique=False, nullable=True)
    target_aptt_high = Column(Integer, unique=False, nullable=True)
    solution_heparin_iu = Column(Integer, unique=False, nullable=True)
    solution_ml = Column(Integer, unique=False, nullable=True)
    tddi = Column(Integer, unique=False, nullable=True)
    target_glycemia = Column(Integer, unique=False, nullable=True)
    other_params = Column(JSONB, unique=False, nullable=True)
    created_at = Column(DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    PrimaryKeyConstraint(name=get_primary_key_name(__tablename__))

    def __init__(
            self,
            first_name: str,
            last_name: str,
            date_of_birth: datetime,
            height: int,
            weight: int,
            sex: int,
            active: bool,
            heparin: bool,
            insulin: bool,
            target_aptt_low: int,
            target_aptt_high: int,
            solution_heparin_iu: int,
            solution_ml: int,
            tddi: int,
            target_glycemia: int,
            other_params: dict
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.height = height
        self.weight = weight
        self.sex = sex
        self.active = active
        self.heparin = heparin
        self.insulin = insulin
        self.target_aptt_low = target_aptt_low
        self.target_aptt_high = target_aptt_high
        self.solution_heparin_iu = solution_heparin_iu
        self.solution_ml = solution_ml
        self.tddi = tddi
        self.target_glycemia = target_glycemia
        self.other_params = other_params
