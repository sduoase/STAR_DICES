import unittest

from monolith.app import create_app
 
class TestHelper(unittest.TestCase):
    def setUp(self):
        self.app = create_app(test=True)
        self.context = self.app.app_context()
        self.app = self.app.test_client()

    def tearDown(self):
        with self.context:
            db.drop_all()

    def _login(self, email, password):
        return self.app.post('/login', data={
            'email': email,
            'password': password
        })

    def _signup(self, email, password, first_name, last_name, birthday):
        return self.app.post('/signup', data={
            'email': email,
            'firstname': first_name,
            'lastname': last_name,
            'password': password,
            'dateofbirth': birthday
        })

    def _logout(self):
        return self.app.get('/logout')
