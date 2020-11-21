# pylint: disable=no-self-use
# Can not, the methods here need self due to the annotations. They are used for generating swagger which needs class.
import logging

from flask import request
from flask_restx import Resource, fields, Namespace

from backend.api.v1.heparin_recommendation_dto_out import heparin_recommendation_out, heparin_recommendation_to_out
from backend.api.v1.shared_models import failed_response
from backend.common.db.model.aptt_values import ApttValue
from backend.common.db.repository.aptt_value_repository import ApttValueRepository
from backend.common.db.repository.heparin_dosage_repository import HeparinDosageRepository
from backend.common.db.repository.patient_repository import PatientRepository
from backend.heparin.heparin_dosage import recommended_heparin

logger = logging.getLogger(__name__)

# create the namespace
namespace = Namespace('heparin-recommendation')

# shared models
heparin_recommendation_out_model = namespace.model('HeparinRecommendationOut', heparin_recommendation_out)


@namespace.route('/recommendation')
class HeparinRecommendationApi(Resource):
    heparin_recommendation_in_model = namespace.model('HeparinRecommendationIn', {
        'patient_id': fields.Integer(required=True),
        'current_aptt': fields.Float(required=True),
    })

    @namespace.doc(body=heparin_recommendation_in_model)
    @namespace.response(code=200, model=heparin_recommendation_out_model,
                        description='Heparin recommendation.')
    @namespace.response(code=400, model=failed_response, description='Wrong data format.')
    @namespace.response(code=401, model=failed_response, description='Authentication failed.')
    @namespace.response(code=500, model=failed_response, description='Unexpected error, see contents for details.')
    def post(self):
        post_data = request.get_json()
        patient_id = int(post_data['patient_id'])

        pa = PatientRepository.get_by_id(patient_id)
        if pa is None:
            return None

        current_aptt = float(post_data['current_aptt'])

        ApttValueRepository.create(ApttValue(
            patient=pa,
            aptt_value=current_aptt
        ))

        previous_aptt = ApttValueRepository.get_newest_by_patient_id(pa.id)

        current_dosage = HeparinDosageRepository.get_newest_by_patient_id(pa.id)
        previous_dosage = HeparinDosageRepository.get_second_newest_by_patient_id(pa.id)

        is_heparin = pa.heparin

        return heparin_recommendation_to_out(recommended_heparin(
            weight=float(pa.weight),
            target_aptt_low=float(pa.target_aptt_low),
            target_aptt_high=float(pa.target_aptt_high) if is_heparin else None,
            current_aptt=current_aptt,
            previous_aptt=None if previous_aptt is None else float(previous_aptt.aptt_value),
            solution_heparin_units=float(pa.solution_heparin_iu),
            solution_ml=float(pa.solution_ml) if is_heparin else None,
            current_continuous_dosage=None if current_dosage is None else float(
                current_dosage.dosage_heparin_continuous),
            previous_continuous_dosage=None if previous_dosage is None else float(
                previous_dosage.dosage_heparin_continuous)
        ))
