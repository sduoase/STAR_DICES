from monolith.app import create_app # pragma: no cover
from monolith.database import db # pragma: no cover
from flask_testing import TestCase # pragma: no cover
 
class TestHelper(TestCase): # pragma: no cover
    def create_app(self):
        self.app = create_app(test=True)
        self.context = self.app.app_context()
        self.client = self.app.test_client()
        return self.app

    def tearDown(self):
        with self.context:
            db.drop_all()

    def _login(self, email, password, follow_redirects=False):
        return self.client.post('/login', follow_redirects=follow_redirects, data={
            'email': email,
            'password': password
        })

    def _signup(self, email, password, first_name, last_name, birthday, follow_redirects=False):
        return self.client.post('/signup', follow_redirects=follow_redirects, data={
            'email': email,
            'firstname': first_name,
            'lastname': last_name,
            'password': password,
            'dateofbirth': birthday
        })

    def _logout(self, follow_redirects=False):
        return self.client.get('/logout', follow_redirects=follow_redirects)
