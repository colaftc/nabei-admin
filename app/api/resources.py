from flask_restful import Resource, fields, marshal_with
from app.repositories import ExpenditureRepo
from flask_restful import reqparse
import decimal
import datetime


expenditure_fields = {
    'name': fields.String,
    'amount': fields.Price,
    'pay_date': fields.DateTime,
    'category': fields.String,
}


parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('category', type=str)
parser.add_argument('amount', type=decimal.Decimal, help='must be a number')
parser.add_argument('pay_date', type=datetime.datetime)


class ExpenditureResource(Resource):
    @marshal_with(expenditure_fields)
    def get(self):
        return ExpenditureRepo().all()

    def post(self):
        args = parser.parse_args()

        try:
            ExpenditureRepo().add(
                name=args['name'],
                amount=args['amount'],
                pay_date=args['pay_date'],
                category=args['category']
            )
        except ValueError as ve:
            return {'message': 'invalid value'}, 400
        except Exception as e:
            return {'message': 'unknown error'}, 500
        else:
            return {'message': 'object created'}, 201
