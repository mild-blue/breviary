# pylint: disable=no-self-use
# Can not, the methods here need self due to the annotations. They are used for generating swagger which needs class.
import logging

from flask import request
from flask_restx import Resource, fields, Namespace

from backend.api.v1.heparin_recommendation_dto_out import heparin_recommendation_out
from backend.api.v1.shared_models import failed_response
from backend.heparin.heparin_dosage import recommended_heparin

logger = logging.getLogger(__name__)

# create the namespace
namespace = Namespace('heparin-recommendation')

# shared models
heparin_recommendation_out_model = namespace.model('HeparinRecommendationOut', heparin_recommendation_out)


@namespace.route('/heparin-recommendation')
class HeparinRecommendationApi(Resource):
    heparin_recommendation_in_model = namespace.model('HeparinRecommendationIn', {
        'weight': fields.Float(required=True),
        'target_aptt_low': fields.Float(required=True),
        'target_aptt_high': fields.Float(required=True),
        'current_aptt': fields.Float(required=True),
        'previous_aptt': fields.Float(required=True),
        'solution_heparin_units': fields.Float(required=True),
        'solution_ml': fields.Float(required=True)
    })

    @namespace.doc(body=heparin_recommendation_in_model)
    @namespace.response(code=200, model=heparin_recommendation_out_model,
                        description='Heparin recommendation.')
    @namespace.response(code=400, model=failed_response, description='Wrong data format.')
    @namespace.response(code=401, model=failed_response, description='Authentication failed.')
    @namespace.response(code=500, model=failed_response, description='Unexpected error, see contents for details.')
    def post(self):
        post_data = request.get_json()
        return recommended_heparin(
            weight=float(post_data['weight']),
            target_aptt_low=float(post_data['target_aptt_low']),
            target_aptt_high=float(post_data['target_aptt_high']),
            current_aptt=float(post_data['current_aptt']),
            previous_aptt=float(post_data['previous_aptt']),
            solution_heparin_units=float(post_data['solution_heparin_units']),
            solution_ml=float(post_data['solution_ml'])
        )
