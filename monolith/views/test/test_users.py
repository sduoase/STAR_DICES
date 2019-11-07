from monolith.views.test.TestHelper import TestHelper

class TestAuth(TestHelper):

    def test_login_required_my_wall(self):
        reply = self.client.get('/my_wall')
        self.assertEqual(reply.status_code, 401)

        reply = self._login("example@example.com", "admin")
        self.assertEqual(reply.status_code, 302)

        reply =  self.client.get('/my_wall')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("mywall.html")

    def test_login_required_users(self):
        reply = self.client.get('/users')
        self.assertEqual(reply.status_code, 401)

        reply = self._login("example@example.com", "admin")
        self.assertEqual(reply.status_code, 302)

        reply =  self.client.get('/users')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("users.html")

        
    def test_login_required_public_wall(self):
        reply = self.client.get('/wall/1')
        self.assertEqual(reply.status_code, 401)

        reply = self._login("example@example.com", "admin")
        self.assertEqual(reply.status_code, 302)

        reply =  self.client.get('/wall/1')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("wall.html")

    def test_login_required_follow(self):
        reply = self.client.get('/wall/1/follow')
        self.assertEqual(reply.status_code, 401)

        reply = self._login("example@example.com", "admin")
        self.assertEqual(reply.status_code, 302)

        reply =  self.client.get('/wall/1/follow')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("message.html")
        self.assert_context("message", "Cannot follow yourself")

    def test_login_required_unfollow(self):
        reply = self.client.get('/wall/1/unfollow')
        self.assertEqual(reply.status_code, 401)

        reply = self._login("example@example.com", "admin")
        self.assertEqual(reply.status_code, 302)

        reply =  self.client.get('/wall/1/unfollow')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("message.html")
        self.assert_context("message", "Cannot unfollow yourself")

    def test_login_required_my_followers(self):
        reply = self.client.get('/my_wall/followers')
        self.assertEqual(reply.status_code, 401)

        reply = self._login("example@example.com", "admin")
        self.assertEqual(reply.status_code, 302)

        reply =  self.client.get('/my_wall/followers')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("myfollowers.html")

    def test_nonexistant_public_wall(self):
        reply = self._login("example@example.com", "admin")
        self.assertEqual(reply.status_code, 302)

        reply =  self.client.get('/wall/2')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("message.html")
        self.assert_context("message", "Ooops.. Writer not found!")

    def test_follow_nonexistant_user(self):
        reply = self._login("example@example.com", "admin")
        self.assertEqual(reply.status_code, 302)

        reply =  self.client.get('/wall/2/follow')
        self.assertEqual(reply.status_code, 404)

    def test_unfollow_nonexistant_user(self):
        reply = self._login("example@example.com", "admin")
        self.assertEqual(reply.status_code, 302)

        reply =  self.client.get('/wall/2/unfollow')
        self.assertEqual(reply.status_code, 404)

    def test_follow_unfollow_existing_user(self):
        reply = self._signup("test123@test.com", "verysecurepassword", "Test", "Script", "10/10/1999")
        self.assertEqual(reply.status_code, 302)

        reply = self._login("test123@test.com", "verysecurepassword", True)
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("home.html")

        reply =  self.client.get('/wall/1/follow')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("message.html")
        self.assert_context("message", "Following!")

        reply =  self.client.get('/wall/1/follow')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("message.html")
        self.assert_context("message", "Already following!")

        reply =  self.client.get('/wall/1/unfollow')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("message.html")
        self.assert_context("message", "Unfollowed!")

        reply =  self.client.get('/wall/1/unfollow')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("message.html")
        self.assert_context("message", "You were not following that particular user!")
