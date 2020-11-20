from sqlalchemy import Column, Integer, DateTime, func, PrimaryKeyConstraint, \
    ForeignKey  # pylint: disable=import-error
from sqlalchemy.orm import RelationshipProperty, relationship

from backend.common.db.base import Base
from backend.common.db.model.patient import Patient
from backend.common.db.model_utils import get_primary_key_name, get_foreign_key_name


class GlycemiaValue(Base):
    """
    GlycemiaValue class
    """
    __tablename__ = "glycemia_value"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    patient_id = Column(
        Integer,
        ForeignKey(f"{Patient.__tablename__}.id", name=get_foreign_key_name(__tablename__, "patient_id")),
        nullable=False
    )
    patient: RelationshipProperty = relationship(Patient)
    glycemia_value = Column(Integer, unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    PrimaryKeyConstraint(name=get_primary_key_name(__tablename__))

    def __init__(
            self,
            patient: Patient,
            glycemia_value: int,
            dosage_heparin_bolus: int
    ) -> None:
        self.patient = patient
        self.glycemia_value = glycemia_value
