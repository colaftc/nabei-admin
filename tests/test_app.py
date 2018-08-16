from manage import app 

class TestApp:
    def setup_class(self):
        self.app=app
        self.app.config['TESTING']=True
        self.client=self.app.test_client()

    def teardown_class(self):
        pass

    def test_app_exists(self):
        assert self.app

    def test_testing_status(self):
        assert self.app.config['TESTING']

    def test_404_handler(self):
        response=self.client.get('/cannot_found_page')
        assert '<body>' 
        assert response.status_code==404

    def test_catching_testing_url(self):
        response=self.client.get('/testing_running')
        assert '...' in response.data
        assert response.status_code == 201

        self.app.config['TESTING']=False
        response=self.client.get('/testing_running')
        assert response.status_code == 500

