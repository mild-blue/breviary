# pylint: disable=no-self-use
# Can not, the methods here need self due to the annotations. They are used for generating swagger which needs class.
import logging

from flask import request
from flask_restx import Resource, fields, Namespace, abort

from backend.api.v1.shared_models import failed_response
from backend.common.db.model.aptt_values import ApttValue
from backend.common.db.model.glycemia_value import GlycemiaValue
from backend.common.db.model.heparin_dosage import HeparinDosage
from backend.common.db.model.insulin_dosage import InsulinDosage
from backend.common.db.repository.aptt_value_repository import ApttValueRepository
from backend.common.db.repository.glycemia_value_repository import GlycemiaValueRepository
from backend.common.db.repository.heparin_dosage_repository import HeparinDosageRepository
from backend.common.db.repository.insulin_dosage_repository import InsulinDosageRepository
from backend.common.db.repository.patient_repository import PatientRepository
from backend.heparin.heparin_dosage import recommended_heparin, HeparinRecommendation
from backend.insulin.insulin_dosage import recommended_insulin

logger = logging.getLogger(__name__)

# create the namespace
namespace = Namespace('recommendation')

heparin_recommendation_out = {
    'actual_heparin_continuous_dosage': fields.Float(required=True, description='Actual heparin continuous dosage.'),
    'previous_heparin_continuous_dosage': fields.Float(required=True,
                                                       description='Previous heparin continuous dosage.'),
    'actual_heparin_bolus_dosage': fields.Float(required=True, description='Actual heparin bolus dosage.'),
    'previous_heparin_bolus_dosage': fields.Float(required=True, description='Previous heparin bolus dosage.'),
    'next_remainder': fields.DateTime(required=True, description='Next reminder.'),
    'doctor_warning': fields.String(required=False, description='Doctor warning.'),
}


def heparin_recommendation_to_out(
        heparin_recommendation: HeparinRecommendation,
        previous_heparin_continuous_dosage: float,
        previous_heparin_bolus_dosage: float
):
    return {
        'actual_heparin_continuous_dosage': float(heparin_recommendation.heparin_continuous_dosage),
        'previous_heparin_continuous_dosage': previous_heparin_continuous_dosage,
        'actual_heparin_bolus_dosage': float(heparin_recommendation.heparin_bolus_dosage),
        'previous_heparin_bolus_dosage': previous_heparin_bolus_dosage,
        'next_remainder': heparin_recommendation.next_remainder.isoformat(),
        'doctor_warning': heparin_recommendation.doctor_warning
    }


def insulin_recommendation_to_out(insulin_dosage: float):
    return {
        'dosage': insulin_dosage
    }


# shared models
heparin_recommendation_out_model = namespace.model('HeparinRecommendationOut', heparin_recommendation_out)
insulin_recommendation_out_model = namespace.model('InsulinRecommendationOut', {
    'dosage': fields.Float(required=True, description='Dosage if insulin.')
})


@namespace.route('/heparin')
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
            abort(404, f"Patient with id {patient_id} does not exist.")

        if not pa.heparin:
            abort(400, f"Patient {patient_id} is not on HEPARIN.")

        current_aptt = float(post_data['current_aptt'])
        previous_aptt = ApttValueRepository.get_newest_by_patient_id(pa.id)

        ApttValueRepository.create(ApttValue(
            patient=pa,
            aptt_value=current_aptt
        ))

        current_dosage = HeparinDosageRepository.get_newest_by_patient_id(pa.id)
        previous_dosage = HeparinDosageRepository.get_second_newest_by_patient_id(pa.id)

        heparin_recommendation = recommended_heparin(
            weight=float(pa.weight),
            target_aptt_low=float(pa.target_aptt_low),
            target_aptt_high=float(pa.target_aptt_high),
            current_aptt=current_aptt,
            previous_aptt=None if previous_aptt is None else float(previous_aptt.aptt_value),
            solution_heparin_units=float(pa.solution_heparin_iu),
            solution_ml=float(pa.solution_ml),
            current_continuous_dosage=None if current_dosage is None else float(
                current_dosage.dosage_heparin_continuous),
            previous_continuous_dosage=None if previous_dosage is None else float(
                previous_dosage.dosage_heparin_continuous)
        )

        logger.info(
            f"Recommendation. Pump speed: {heparin_recommendation.heparin_continuous_dosage}, bolus: {heparin_recommendation.heparin_bolus_dosage}, next remainder {heparin_recommendation.next_remainder}, warning: {heparin_recommendation.doctor_warning}.")

        HeparinDosageRepository.create(HeparinDosage(
            patient=pa,
            dosage_heparin_continuous=heparin_recommendation.heparin_continuous_dosage,
            dosage_heparin_bolus=heparin_recommendation.heparin_bolus_dosage
        ))

        return heparin_recommendation_to_out(
            heparin_recommendation=heparin_recommendation,
            previous_heparin_continuous_dosage=None if current_dosage is None else float(
                current_dosage.dosage_heparin_continuous),
            previous_heparin_bolus_dosage=None if current_dosage is None else float(
                current_dosage.dosage_heparin_bolus)
        )


@namespace.route('/insulin')
class InsulinRecommendationApi(Resource):
    insulin_recommendation_in_model = namespace.model('InsulinRecommendationIn', {
        'patient_id': fields.Integer(required=True),
        'current_glycemia': fields.Integer(required=True),
        'expected_carbohydrate_intake': fields.Float(required=True),
    })

    @namespace.doc(body=insulin_recommendation_in_model)
    @namespace.response(code=200, model=insulin_recommendation_out_model,
                        description='Insulin recommendation.')
    @namespace.response(code=400, model=failed_response, description='Wrong data format.')
    @namespace.response(code=401, model=failed_response, description='Authentication failed.')
    @namespace.response(code=500, model=failed_response, description='Unexpected error, see contents for details.')
    def post(self):
        post_data = request.get_json()
        patient_id = int(post_data['patient_id'])

        pa = PatientRepository.get_by_id(patient_id)
        if pa is None:
            abort(404, f"Patient with id {patient_id} does not exist.")

        if not pa.insulin:
            abort(400, f"Patient {patient_id} is not on INSULIN.")

        current_glycemia = float(post_data['current_glycemia'])

        GlycemiaValueRepository.create(GlycemiaValue(
            patient=pa,
            glycemia_value=current_glycemia
        ), False)

        insulin_recommendation = recommended_insulin(
            tddi=float(pa.tddi),
            target_glycemia=float(pa.target_glycemia),
            current_glycemia=current_glycemia,
            expected_carbohydrate_intake=float(post_data['expected_carbohydrate_intake'])
        )

        logger.info(
            f"Recommendation. Dosage: {insulin_recommendation}.")

        InsulinDosageRepository.create(InsulinDosage(
            patient=pa,
            dosage_insulin=insulin_recommendation
        ))

        return insulin_recommendation_to_out(insulin_recommendation)
