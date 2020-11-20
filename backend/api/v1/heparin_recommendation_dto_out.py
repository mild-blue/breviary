# pylint: disable=no-self-use
# Can not, the methods here need self due to the annotations. They are used for generating swagger which needs class.

from flask_restx import fields

heparin_recommendation_out = {
    'heparin_continuous_dosage': fields.Float(required=True, description='Heparin countinuous dosage.'),
    'heparin_bolus_dosage': fields.Float(required=True, description='Heparin bolus dosage.'),
    'next_remainder': fields.DateTime(required=True, description='Next reminder.'),
    'doctor_warning': fields.String(required=False, description='Doctor warning.'),
}
