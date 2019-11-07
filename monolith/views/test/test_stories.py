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
        with self.context:
            s = Story.query.filter_by(id=1).first()
            self.assertIsNone(s)
        
    def test_random_story(self):
        
        # error: no random story
        self._login("example@example.com", "admin")
        reply = self.client.get('/story/1/delete')
        reply = self.client.get('/random_story')
        self.assert_template_used("story.html")
        self.assert_context("message", "Ooops.. No random story for you!")
        
    def test_new_story(self):
        
        # success: render new_story.html
        self._login("example@example.com", "admin")
        reply = self.client.get('/stories/new_story')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("new_story.html")
        
        # success: add a record in db
        reply = self.client.post('/stories/new_story', data={ "theme" : "Mountain", "dice_number" : "3"})
        self.assertEqual(reply.status_code, 302)
        with self.context:
            s = Story.query.filter_by(id=2).first()
            self.assertIsNotNone(s)
            
        # error: must first publish, no new record
        reply = self.client.post('/stories/new_story', data={ "theme" : "Mountain", "dice_number" : "3"})
        self.assertEqual(reply.status_code, 302)
        with self.context:
            s = Story.query.filter_by(id=3).first()
            self.assertIsNone(s)
            
    def test_write_story(self):
        
        # error: story id not valid
        self._login("example@example.com", "admin")
        reply = self.client.get('/write_story/3')
        self.assertEqual(reply.status_code, 404)
        
        # error: I'm not author
        self._logout()
        self._signup("fantastic@example.com", "betterNerfIrelia", "404", "404", "01/01/1964", True)
        self._login("fantastic@example.com", "betterNerfIrelia")
        reply = self.client.post('/stories/new_story', data={ "theme" : "Mountain", "dice_number" : "3"})
        with self.context:
            s = Story.query.filter_by(id=2).first()
            self.assertIsNotNone(s)
        self._logout()
        self._login("example@example.com", "admin")
        reply = self.client.get('/write_story/2')
        self.assertEqual(reply.status_code, 401)
        
        # success: render write_story.html
        self._logout()
        self._login("fantastic@example.com", "betterNerfIrelia")
        reply = self.client.get('/write_story/2')
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("/write_story.html")

        # error: title needed
        reply = self.client.post('/write_story/2', data={
                 'text' : "Mountain",
                 'title' : "",
                 'store_story' : 1})
        self.assert_context("message", "You must complete the title in order to publish the story")
        self.assertEqual(reply.status_code, 200)

        # error: story not valid
        reply = self.client.get('/write_story/2')
        self.assertEqual(reply.status_code, 200)
        reply = self.client.post('/write_story/2', data={
                 'text' : "1",
                 'title' : "ThisIsATitle",
                 'store_story' : 1})
        self.assert_context("message", "You must use all the words of the outcome!")
        
        # success: written draft
        reply = self.client.get('/write_story/2')
        self.assertEqual(reply.status_code, 200)
        reply = self.client.post('/write_story/2', data={
                 'text' : "1",
                 'title' : "ThisIsATitle",
                 'store_story' : 0})
        self.assert_template_used("/write_story.html")      
        
        
        
