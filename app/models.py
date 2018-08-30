from extentions import exts
from sqlalchemy import func
from flask_mongoengine import Document
import datetime

db = exts['db']
mdb = exts['mdb']


CATEGORY_CHOICES_MAP = {
    'H': '货款',
    'Y': '运费',
    'Z': '租金',
    'G': '工资',
    'B': '包装耗材',
    'Q': '其它',
}


CATEGORY_CHOICES = [(k, v) for k, v in CATEGORY_CHOICES_MAP.items()]


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


class ExpenditureDocument(Document):
    name = mdb.StringField(max_length=200, required=True)
    amount = mdb.DecimalField(pricision=2, required=True)
    category = mdb.StringField(max_length=20, required=True, default='Q', choices=CATEGORY_CHOICES)
    pay_date = mdb.DateTimeField(required=True, default=datetime.datetime.now)
    meta = {'strict': False}

    def category_label(self):
        return CATEGORY_CHOICES_MAP[self.category]

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<ExpenditureDocument name={} amount={} category={}>'.format(self.name, self.amount, self.category)

    def to_dict(self):
        return {
            'name': self.name,
            'amount': self.amount,
            'category': self.category,
            'pay_date': self.pay_date
        }
