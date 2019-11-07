from monolith.views.test.TestHelper import TestHelper
from monolith.database import db, User, Story

class TestAuth(TestHelper):


    def test_home(self):
    
        # error: user anonymous
        reply = self.client.get('/', follow_redirects=True)
        self.assert_template_used("login.html")
        
        # success: render home.html
        self._login("example@example.com", "admin")
        reply = self.client.get('/', follow_redirects=True)
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("home.html")
        
    def test_explore(self):
        
        # error: user anonymous
        reply = self.client.get('/explore', follow_redirects=True)
        self.assert_template_used("login.html")
        
        # success: render explore.html
        self._login("example@example.com", "admin")
        reply = self.client.get('/explore', follow_redirects=True)
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("explore.html")
        
        # TODO DATE FILTER
        
    def test_single_story(self):
        
        # error: user anonymous
        reply = self.client.get('/story/1', follow_redirects=True)
        self.assertEqual(reply.status_code, 401)
        
        # error: story_id not valid
        self._login("example@example.com", "admin")
        reply = self.client.get('/story/5', follow_redirects=True)
        self.assert_template_used("message.html")
        self.assert_context("message", "Ooops.. Story not found!")
        
        # success: render story.html
        reply = self.client.get('/story/1', follow_redirects=True)
        self.assert_template_used("story.html")
        
    def test_delete_story(self):
        
        # error: story_id not valid
        self._login("example@example.com", "admin")
        reply = self.client.get('/story/5/delete')
        self.assertEqual(reply.status_code, 404)
        
        # error: user not author
        self._logout()
        self._signup("example3@example.com", "thecakeisalie", "GLaDOS", "unknown", "01/01/1964", True)
        self._login("example3@example.com", "thecakeisalie")
        reply = self.client.get('/story/1/delete')
        self.assertEqual(reply.status_code, 401)
        
        # success: render message.html
        self._logout()
        self._login("example@example.com", "admin")
        reply = self.client.get('/story/1/delete')
        self.assert_template_used("message.html")
        self.assert_context("message", "Story sucessfully deleted")
        
    def test_random_story(self):
    
        # success: render the random story
        #TODO
        #self._login("example@example.com", "admin")
        #reply = self.client.get('/random_story')
        #self.assert_template_used("story.html")
        #self.assert_context("rolls_outcome", "[]")
        
        # error: no random story
        self._login("example@example.com", "admin")
        reply = self.client.get('/story/1/delete')
        reply = self.client.get('/random_story')
        self.assert_template_used("story.html")
        self.assert_context("message", "Ooops.. No random story for you!")
        
        
