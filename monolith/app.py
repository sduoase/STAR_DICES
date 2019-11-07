import datetime
import json
import os

from monolith.database import db, User, Story, Dice, retrieve_dice_set, retrieve_themes, store_dice_set
from monolith.classes.DiceSet import DiceSet
from monolith.auth import login_manager
from monolith.views import blueprints
from monolith.classes.Die import Die
from monolith import celeryApp

from flask import Flask, jsonify

def create_app(test = False):
    app = Flask(__name__, static_url_path='/static')
    app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    app.config['SECRET_KEY'] = 'ANOTHER ONE'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storytellers.db'
    if test:
        app.config['TESTING'] = True
        app.config['CELERY_ALWAYS_EAGER'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    celery = celeryApp.make_celery(app)
    celeryApp.celery = celery
    
    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    db.init_app(app)
    login_manager.init_app(app)
    db.create_all(app=app)

    with app.app_context():
        # Create first admin user.
        q = db.session.query(User).filter(User.email == 'example@example.com')
        user = q.first()
        if user is None:
            example = User()
            example.firstname = 'Admin'
            example.lastname = 'Admin'
            example.email = 'example@example.com'
            example.dateofbirth = datetime.datetime(2020, 10, 5)
            example.is_admin = True
            example.set_password('admin')
            db.session.add(example)
            db.session.commit()
	
            example = Story()
            example.title = 'My first story!'
            example.rolls_outcome = '[["bike", "static/Mountain/bike.PNG"], ["bus", "static/Mountain/bus.PNG"]]'
            example.text = 'With my bike, I am faster than a bus!!!!'
            example.theme = 'Mountain'
            example.published = 1
            example.likes = 42
            example.dislikes = 5
            example.author_id = 1
            db.session.add(example)
            db.session.commit() 

        # Create dice sets if missing.
        themes = retrieve_themes()
        if not themes:
            die1 = Die(
                ['angry', 'bag', 'bike', 'bird', 'crying', 'moonandstars'],
                "N/A"
            )
            die2 = Die(
                ['bus', 'coffee', 'happy', 'letter', 'paws', 'plate'],
                "N/A"
            )
            die3 = Die(
                ['caravan', 'clock', 'drink', 'mouth', 'tulip', 'whale'],
                "N/A"
            )
            die4 = Die(
                ['baloon', 'bananas', 'cat', 'icecream', 'pencil', 'phone'],
                "N/A"
            )
            dice_set = DiceSet([die1, die2, die3], "Mountain")
            store_dice_set(dice_set)
            dice_set = DiceSet([die2, die3, die4], "Late night")
            store_dice_set(dice_set)
            dice_set = DiceSet([die3, die1, die4], "Travelers")
            store_dice_set(dice_set)
            dice_set = DiceSet([die2, die1, die4], "Youth")
            store_dice_set(dice_set)
            die = Die(["1", "2", "3"], "test_theme")
            dice_set = DiceSet([die], "test_theme")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
