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

    def _login(self, email, password, follow_redirects=False):
        return self.app.post('/login', follow_redirects=follow_redirects, data={
            'email': email,
            'password': password
        })

    def _signup(self, email, password, first_name, last_name, birthday, follow_redirects=False):
        return self.app.post('/signup', follow_redirects=follow_redirects, data={
            'email': email,
            'firstname': first_name,
            'lastname': last_name,
            'password': password,
            'dateofbirth': birthday
        })

    def _logout(self, follow_redirectsFalse):
        return self.app.get('/logout', follow_redirects=follow_redirects)
