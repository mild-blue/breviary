# pylint: disable=no-self-use
# Can not, the methods here need self due to the annotations. They are used for generating swagger which needs class.
import datetime
import logging

from flask import request
from flask_restx import Resource, Namespace, fields, abort

from backend.api.v1.heparin_recommendation_dto_out import heparin_recommendation_out, heparin_recommendation_to_out
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
    'high': fields.Float(requred=True),
})

patient_out = namespace.model('PatientOut', {
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
    'previous_aptt': fields.Float(required=True),
    'actual_dosage': fields.Float(required=True),
    'previous_dosage': fields.Float(required=True),
})

patient_in = namespace.model('PatientIn', {
    'id': fields.String(required=True)
})

patient_in_update = namespace.model('PatientInUpdate', {
    'drug_type': fields.String(required=True, enum=[drug.value for drug in DrugType]),
    'target_aptt_low': fields.Float(required=False),  # HEPARIN
    'target_aptt_high': fields.Float(required=False),  # HEPARIN
    'tddi': fields.Float(required=False),  # INSULIN
    'target_glycemia': fields.Float(required=False)  # INSULIN
})


@namespace.route('/')
class PatientsLists(Resource):
    model = namespace.model('PatientsData', {
        'patients': fields.List(required=True, cls_or_instance=fields.Nested(patient_out)),
    })

    @namespace.response(code=200,
                        model=model,
                        description='')
    @namespace.response(code=500,
                        model=failed_response,
                        description='Unexpected error, see contents for details.')
    def get(self):
        patients = PatientRepository.get_all_active()
        result = []
        for pa in patients:
            result.append(_patient_model_to_dto(pa))

        return result

    @namespace.doc(body=patient_in)
    @namespace.response(code=200, model=patient_out, description='')
    @namespace.response(code=400, model=failed_response, description='')
    @namespace.response(code=401, model=failed_response, description='')
    @namespace.response(code=500, model=failed_response, description='')
    def post(self):
        post_data = request.get_json()
        dummy_patient_id = post_data['id']
        pa = PatientRepository.get_first_inactive_patient()

        if pa is None:
            abort(404, f"Patient does not exist.")

        pa.active = True
        pa = PatientRepository.base_update(pa)
        return _patient_model_to_dto(pa)


@namespace.route('/<patient_id>')
class Patient(Resource):
    model = patient_out

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

    @namespace.doc(body=patient_in_update)
    @namespace.response(code=200, model=patient_out, description='')
    @namespace.response(code=400, model=failed_response, description='')
    @namespace.response(code=401, model=failed_response, description='')
    @namespace.response(code=500, model=failed_response, description='')
    def put(self, patient_id: str):
        patient_id = int(patient_id)
        pa = PatientRepository.get_by_id(patient_id)
        if pa is None:
            abort(404, f"Patient with id {patient_id} does not exist.")

        put_data = request.get_json()
        if put_data['drug_type'] == DrugType.HEPARIN:
            pa.heparin = True
            pa.insulin = False
            pa.target_aptt_low = float(put_data['target_aptt_low'])
            pa.target_aptt_high = float(put_data['target_aptt_high'])
        else:
            pa.heparin = False
            pa.insulin = True
            pa.tddi = float(put_data['tddi'])
            pa.target_glycemia = float(put_data['target_glycemia'])

        pa = PatientRepository.base_update(pa)
        return _patient_model_to_dto(pa)


history_entry_out = namespace.model('HistoryEntry', {
    'date': fields.DateTime(required=True),
    'aptt': fields.Float(required=True),
    'bolus': fields.Float(required=True),
    'heparin_continuous': fields.Float(required=True)
})


@namespace.route('/history-entries/<patient_id>')
class Recommendation(Resource):
    model = namespace.model('HistoryEntries', {
        'entries': fields.List(required=True, cls_or_instance=fields.Nested(history_entry_out)),
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

        min_len = min(len(dosages), len(aptts))
        result = []

        for i in range(0, min_len):
            dosage = dosages[i]
            aptt = aptts[i]
            result.append({
                'date': dosage.created_at.isoformat(),
                'aptt': float(aptt.aptt_value),
                'bolus': float(dosage.dosage_heparin_bolus),
                'heparin_continuous': float(dosage.dosage_heparin_continuous)
            })

        return result


def _patient_model_to_dto(pa: Patient) -> dict:
    if pa is None:
        abort(404, f"Patient does not exist.")

    actual_aptt = ApttValueRepository.get_newest_by_patient_id(pa.id)
    previous_aptt = ApttValueRepository.get_second_newest_by_patient_id(pa.id)

    actual_heparin_dosage = HeparinDosageRepository.get_newest_by_patient_id(pa.id)
    previous_heparin_dosage = HeparinDosageRepository.get_second_newest_by_patient_id(pa.id)
    is_heparin = pa.heparin

    return {
        'id': pa.id,
        'first_name': pa.first_name,
        'last_name': pa.last_name,
        'date_of_birth': pa.date_of_birth.isoformat(),
        'height': float(pa.height),
        'weight': float(pa.weight),
        'sex': pa.sex,
        'drug_type': DrugType.HEPARIN if pa.heparin else DrugType.INSULIN,
        'target_aptt': {
            'low': float(pa.target_aptt_low) if is_heparin else None,
            'high': float(pa.target_aptt_high) if is_heparin else None
        },
        'actual_aptt': None if actual_aptt is None else float(actual_aptt.aptt_value),
        'actual_aptt_updated_on': datetime.date(1970, 1,
                                                1).isoformat() if actual_aptt is None else actual_aptt.created_at.isoformat(),
        'previous_aptt': None if previous_aptt is None else float(previous_aptt.aptt_value),
        'actual_dosage': None if actual_heparin_dosage is None else float(actual_heparin_dosage.dosage_heparin_continuous),
        'previous_dosage': None if previous_heparin_dosage is None else float(previous_heparin_dosage.dosage_heparin_continuous)
    }
