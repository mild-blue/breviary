# pylint: disable=no-self-use
# Can not, the methods here need self due to the annotations. They are used for generating swagger which needs class.

from flask_restx import fields

from backend.heparin.heparin_dosage import HeparinRecommendation

heparin_recommendation_out = {
    'actual_heparin_continuous_dosage': fields.Float(required=True, description='Actual heparin continuous dosage.'),
    'previous_heparin_continuous_dosage': fields.Float(required=True, description='Previous heparin continuous dosage.'),
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
