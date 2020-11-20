# pylint: disable=no-self-use
# Can not, the methods here need self due to the annotations. They are used for generating swagger which needs class.
import datetime
import logging

from flask_restx import Resource, Namespace, fields

from backend.api.v1.heparin_recommendation_dto_out import heparin_recommendation_out
from backend.api.v1.shared_models import failed_response
from backend.common.db.model.enums import Sex, DrugType
from backend.common.db.repository.aptt_value_repository import ApttValueRepository
from backend.common.db.repository.heparin_dosage_repository import HeparinDosageRepository
from backend.common.db.repository.patient_repository import PatientRepository
from backend.heparin.heparin_dosage import recommended_heparin

logger = logging.getLogger(__name__)

namespace = Namespace('patients')

heparin_recommendation_out_model = namespace.model('HeparinRecommendationOut', heparin_recommendation_out)

target_aptt = namespace.model('TargetAptt', {
    'low': fields.Float(requred=True),
    '': fields.Float(requred=True),
})

patient = namespace.model('Patient', {
    'id': fields.Integer(required=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'date_of_birth': fields.Date(required=True),
    'height': fields.Integer(required=True, description='In CM'),
    'weight': fields.Float(required=True, description='In KG'),
    'sex': fields.String(required=True, enum=[sex.value for sex in Sex]),
    'drug_type': fields.String(required=True, enum=[drug.value for drug in DrugType]),
    'target_aptt': fields.Nested(target_aptt),
    'actual_aptt': fields.Float(required=True),
    'actual_aptt_updated_on': fields.DateTime(required=True),
    'actual_dosage': fields.Float(required=True),
})


@namespace.route('/')
class PatientsLists(Resource):
    model = namespace.model('PatientsData', {
        'patients': fields.List(required=True, cls_or_instance=fields.Nested(patient)),
    })

    @namespace.response(code=200,
                        model=model,
                        description='')
    @namespace.response(code=500,
                        model=failed_response,
                        description='Unexpected error, see contents for details.')
    def get(self):
        patients = PatientRepository.get_all()
        result = []
        for pa in patients:
            result.append(_patient_model_to_dto(pa))

        return result


@namespace.route('/<patient_id>')
class Patient(Resource):
    model = patient

    @namespace.response(code=200,
                        model=model,
                        description='')
    @namespace.response(code=500,
                        model=failed_response,
                        description='Unexpected error, see contents for details.')
    def get(self, patient_id: str):
        patient_id = int(patient_id)
        pa = PatientRepository.get_by_id(patient_id)
        return _patient_model_to_dto(pa)


@namespace.route('/recommendation/<patient_id>')
class Recommendation(Resource):
    @namespace.response(code=200,
                        model=heparin_recommendation_out_model,
                        description='')
    @namespace.response(code=500,
                        model=failed_response,
                        description='Unexpected error, see contents for details.')
    def get(self, patient_id: str):
        patient_id = int(patient_id)
        pa = PatientRepository.get_by_id(patient_id)
        if pa is None:
            return None

        current_aptt = ApttValueRepository.get_newest_by_patient_id(pa.id)
        previous_appt = ApttValueRepository.get_second_newest_by_patient_id(pa.id)

        return recommended_heparin(
            weight=pa.weight,
            target_aptt_low=pa.target_aptt_low,
            target_aptt_high=pa.target_aptt_high,
            current_aptt=-1 if current_aptt is None else current_aptt.aptt_value,
            previous_aptt=-1 if previous_appt is None else previous_appt.aptt_value,
            solution_heparin_units=pa.solution_heparin_iu,
            solution_ml=pa.solution_ml
        )


dosage = namespace.model('DosageEntry', {
    'date': fields.DateTime(required=True),
    'value': fields.Float(required=True),
})


@namespace.route('/history-entries/<patient_id>')
class Recommendation(Resource):
    model = namespace.model('HistoryEntries', {
        'dosage_entries': fields.List(required=True, cls_or_instance=fields.Nested(dosage)),
        'aptt_entries': fields.Float(required=True, cls_or_instance=fields.Nested(dosage))
    })

    @namespace.response(code=200,
                        model=model,
                        description='')
    @namespace.response(code=500,
                        model=failed_response,
                        description='Unexpected error, see contents for details.')
    def get(self, patient_id: str):
        patient_id = int(patient_id)
        dosages = HeparinDosageRepository.get_by_patient_id(patient_id)
        aptts = ApttValueRepository.get_by_patient_id(patient_id)

        return {
            'dosage_entries': [{'date': dosage.created_at, 'value': dosage.dosage_heparin_continuous} for dosage in
                               dosages],
            'aptt_entries': [{'date': aptt.created_at, 'value': aptt.aptt_value} for aptt in aptts]
        }


def _patient_model_to_dto(pa: Patient) -> dict:
    if pa is None:
        return None
    actual_appt = ApttValueRepository.get_newest_by_patient_id(pa.id)
    heparin_dosage = HeparinDosageRepository.get_newest_by_patient_id(pa.id)
    return {
        'id': pa.id,
        'first_name': pa.first_name,
        'last_name': pa.last_name,
        'date_of_birth': pa.date_of_birth,
        'height': pa.height,
        'weight': pa.weight,
        'sex': pa.sex,
        'drug_type': DrugType.HEPARIN if pa.heparin else DrugType.INSULIN,
        'target_aptt': {
            'low': pa.target_aptt_low,
            'high': pa.target_aptt_high
        },
        'actual_aptt': -1 if actual_appt is None else actual_appt.aptt_value,
        'actual_aptt_updated_on': datetime.date(1970, 1, 1) if actual_appt is None else actual_appt.created_at,
        'actual_dosage': -1 if heparin_dosage is None else heparin_dosage.dosage_heparin_continuous
    }
