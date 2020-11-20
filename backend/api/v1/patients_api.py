# pylint: disable=no-self-use
# Can not, the methods here need self due to the annotations. They are used for generating swagger which needs class.
import logging

from flask_restx import Resource, Namespace, fields

from backend.api.v1.shared_models import failed_response
from backend.common.db.model.enums import Sex, DrugType

logger = logging.getLogger(__name__)

namespace = Namespace('patients')

target_aptt = namespace.model('TargetAptt', {
    'low': fields.Float(requred=True),
    'high': fields.Float(requred=True),
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
        return {'status': 'ok'}


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
        return {'status': patient_id}


@namespace.route('/recommendation/<patient_id>')
class Recommendation(Resource):
    model = namespace.model('Recommendation', {
        'patient_id': fields.Integer(required=True),
        'recommended_dosage': fields.Float(required=True)
    })

    @namespace.response(code=200,
                        model=model,
                        description='')
    @namespace.response(code=500,
                        model=failed_response,
                        description='Unexpected error, see contents for details.')
    def get(self, patient_id: str):
        patient_id = int(patient_id)
        return {'patient_id': patient_id}


dosage = namespace.model('DosageEntry', {
    'date': fields.DateTime(required=True),
    'value': fields.Float(required=True),
})


@namespace.route('/recommendation/<patient_id>')
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
        return {'patient_id': patient_id}
