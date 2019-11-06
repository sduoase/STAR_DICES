import unittest

from monolith.app import create_app
from monolith.database import db, User, Story, Like, Dislike
 
class TestHelper(unittest.TestCase):
    def setUp(self):
        self.app = create_app(test=True)
        self.context = self.app.app_context()
        self.app = self.app.test_client()

    def tearDown(self):
        with self.context:
            db.drop_all()

    def _login(self, email, password):
        reply = self.app.post('/login', data={
            'email': email,
            'password': password
        })
        return reply.status_code

    def _successful_login(self, email, password):
        # Successful login == redirect to default home page
        self.assertEqual(self._login(email, password), 302)

    def _unsuccessful_login(self, email, password):
        # Unsuccessful login == no redirect and error message
        self.assertEqual(self._login(email, password), 200)

    def _signup(self, email, password, first_name, last_name, birthday):
        reply = self.app.post('/signup', data={
            'email': email,
            'firstname': first_name,
            'lastname': last_name,
            'password': password,
            'dateofbirth': birthday
        })
        return reply.status_code

    def _successful_signup(self, email, password, first_name, last_name, birthday):
        self.assertEqual(self._signup(email, password, first_name, last_name, birthday), 302)

    def _unsuccessful_signup(self, email, password, first_name, last_name, birthday):
        self.assertEqual(self._signup(email, password, first_name, last_name, birthday), 200)

    def _logout(self):
        reply = self.app.get('/logout')
        return reply.status_code

    def test_user_registration(self):
        self._unsuccessful_login('test@script.com', 'verysecurepassword')
        self._successful_signup('test@script.com', 'verysecurepassword', 'Test', 'Script', '03/11/1971')
        self._logout()
        self._unsuccessful_signup('test@script.com', 'verysecurepassword', 'Test', 'Script', '03/11/1971')

