from flask import Blueprint
from flask_restful import Api
from .resources import ExpenditureResource


api_bp = Blueprint('api', __name__)
api = Api(api_bp)
api.add_resource(ExpenditureResource, '/expenditure', endpoint='expenditure')
