# pylint: disable=no-self-use
# Can not, the methods here need self due to the annotations. They are used for generating swagger which needs class.

from flask_restx import fields

from backend.heparin.heparin_dosage import HeparinRecommendation

heparin_recommendation_out = {
    'heparin_continuous_dosage': fields.Float(required=True, description='Heparin continuous dosage.'),
    'heparin_bolus_dosage': fields.Float(required=True, description='Heparin bolus dosage.'),
    'next_remainder': fields.DateTime(required=True, description='Next reminder.'),
    'doctor_warning': fields.String(required=False, description='Doctor warning.'),
}


def heparin_recommendation_to_out(heparinRecommendation: HeparinRecommendation):
    return {
        'heparin_continuous_dosage': float(heparinRecommendation.heparin_continuous_dosage),
        'heparin_bolus_dosage': float(heparinRecommendation.heparin_bolus_dosage),
        'next_remainder': heparinRecommendation.next_remainder.isoformat(),
        'doctor_warning': heparinRecommendation.doctor_warning
    }
