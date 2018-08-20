from app import create_app
from extentions import exts
from app import models
from app.repositories import ExpenditureRepository

db = exts['db']


class TestApp:
    def setup_class(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.init_app(self.app)
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
        assert '<body>' 
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

