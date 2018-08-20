from extentions import exts
from sqlalchemy import func
import datetime

db = exts['db']


class ExpenditureType(db.Model):
    __tablename__ = 'expenditure_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    expenditure = db.relationship('Expenditure', backref='typing')

    def __str__(self):
        return self.name


class Expenditure(db.Model):
    __tablename__ = 'expenditure'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer)
    amount = db.Column(db.Numeric(7, 2))
    paid = db.Column(db.Boolean, default=False)
    pay_date = db.Column(db.Date, default=datetime.date.today)
    mark_date = db.Column(db.DateTime, server_default=func.now())
    type_id = db.Column(db.Integer, db.ForeignKey('expenditure_type.id'))

    def __str__(self):
        return self.name
