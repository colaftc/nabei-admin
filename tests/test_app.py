# -*- coding:utf-8

from app import create_app
from extentions import exts
from app import models
import decimal
import datetime
from app.repositories import ExpenditureRepository, ExpenditureRepo, ExpenditureDocument
from manage import init_app
from app.api.user import ApiUser, ApiUserRepo
from werkzeug.security import check_password_hash

db = exts['db']
mdb = exts['mdb']


class TestApp:
    def setup_class(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.init_app(self.app)
        init_app(self.app)
        db.create_all(app=self.app)

    def teardown_class(self):
        # db.drop_all(app=self.app)
        pass

    def test_app_exists(self):
        assert self.app

    def test_testing_status(self):
        assert self.app.config['TESTING']

    def test_404_handler(self):
        response = self.client.get('/cannot_found_page')
        assert response.status_code == 404

    def test_database_connect(self):
        e = models.ExpenditureType(name='testing')
        db.session.add(e)
        db.session.commit()
        db.session.delete(e)
        db.session.commit()

    def test_expenditure_repository(self):
        repo = ExpenditureRepository(page_size=20)
        repo.add(name='repo_testing')
        assert repo.get_or(19762, None) is None
        assert repo.get_or(66887, 'Not Found') == 'Not Found'
        e = repo.get_by('%repo%')
        e = e[0]
        assert e is not None
        repo.remove(e)


class TestMongoRepo:
    PRESSURE_TIMES = 100

    def setup_class(self):
        self.app = create_app('testing')
        init_app(self.app)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.repo = ExpenditureRepo()

    def test_repo_method(self):
        name = 'testing'
        amount = decimal.Decimal('1969.17')
        item = self.repo.add(name=name, amount=amount, category='B', pay_date=datetime.datetime.now())
        assert item.id is not None
        assert item.name == name
        assert item.amount == amount

        v1 = self.repo.get_by(name='testing')
        v2 = self.repo.get_or('testing')
        assert v1 == v2
        assert v1.category_label() == '包装耗材'
        assert self.repo.get_or('notbefound') is None

        self.repo.remove({'name': 'testing'})
        assert self.repo.get_by(name='testing') is None

    def test_pressure(self):
        for i in range(self.PRESSURE_TIMES):
            self.repo.add(name='pressure_testing{}'.format(i), amount=i*1.1, category='G', pay_date=datetime.datetime.now())

        v = self.repo.get_or('pressure_testing87')
        assert v is not None
        ExpenditureDocument.objects.delete()

    def test_post(self):
        resp = self.client.post('/api/expenditure', data={
            'name': 'testing-post',
            'amount': 1868.55,
            'category': 'Q',
        })
        assert resp.status_code == 201
        assert resp.is_json

        item = self.repo.get_by('testing-post')
        assert item.amount > 1868
        assert models.CATEGORY_CHOICES_MAP[item.category] == '其它'

        self.repo.remove({'name': 'testing-post'})
        assert self.repo.get_or('testing-post') is None

    def test_user(self):
        user = ApiUser.load(101)
        assert user
        assert user.username == 'colaftc'
        assert user.authenticate('fcp0520')
        assert user.is_login
        token = user.generate_token()
        assert token
        assert user.verify_token(token)
        assert user.is_admin
