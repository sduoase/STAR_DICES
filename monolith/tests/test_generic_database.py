import unittest

from monolith.app import create_app
from monolith.database import db, is_date, _deserialize_dice_set, retrieve_themes, isFollowing, getStats, Story, retrieve_dice_set
from monolith.classes.DiceSet import DiceSet
from monolith.classes.Die import Die


class TestDB(unittest.TestCase):

    def setUp(self):
        self.app = create_app(test=True)
        self.context = self.app.app_context()
        self.app = self.app.test_client()
        return self.app

    def tearDown(self):
        with self.context:
            db.drop_all()

    def testIsDate(self):
        self.assertEqual(is_date("2012-03-04"), True)
        self.assertEqual(is_date("2012-55-55"), False)

    def testRetriveDiceSet(self):
        with self.context:
            self.assertEqual(retrieve_dice_set("NonExistingTheme"), None)

    def testRetriveTheme(self):
        with self.context:
            self.assertEqual(retrieve_themes(), ["Mountain", "Late night", "Travelers", "Youth"])

    def testFollowing(self):
        with self.context:
            self.assertEqual(isFollowing(1,1), False)

    def testStats(self):
        with self.context:
            self.assertEqual(getStats(0), 0)
            # tests the stats for user == 1, it has 1 single published story which have 42 likes and 5 dislikes
            self.assertEqual(getStats(1), round(42/5, 2))

            stry = db.session.query(Story).filter(Story.published == 1).first()
            stry.likes = 0
            db.session.commit()

            self.assertEqual(getStats(1), round(1/5, 2))

            stry.dislikes = 0
            db.session.commit()

            self.assertEqual(getStats(1), 1)

