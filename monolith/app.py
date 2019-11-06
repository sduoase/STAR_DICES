import datetime
import json
import os

from flask import Flask, jsonify

from monolith.database import db, User, Story, Dice, retrieve_dice_set, store_dice_set
from monolith.auth import login_manager
from monolith.classes import Die, DiceSet
from monolith import celeryApp
from monolith.views import blueprints

def create_app(test = False):
    app = Flask(__name__)
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

        q = db.session.query(Story)
        story = q.first()
        if story is None:
            example = Story()
            example.title= 'Test title'
            example.rolls_outcome= '["Cat", "Run", "Spring", "Mountain"]'
            example.text = 'Trial cat of run admin user :) but i want to pring more words just to test the mountain'
            example.theme= 'theme1'
            example.published=1
            example.likes = 42
            example.dislikes = 5
            example.author_id = 1
            db.session.add(example)
            example = Story()
            example.title= 'Test title 2'
            example.text = 'Trial story 2 of example admin user :) but i want to add more words just to test that those will be cut out in the home'
            example.theme= 'theme1'
            example.rolls_outcome= '["Cat", "Jump", "Fall", "House"]'
            example.published=0
            example.author_id = 1
            db.session.add(example)
            db.session.commit()

        # Create default dice set.
        dice_set = retrieve_dice_set()
        if dice_set is None:
            die1 = Die.Die(['Dog', 'Cat', 'Horse'])
            die2 = Die.Die(['Jump', 'Sleep', 'Run'])
            die3 = Die.Die(['Summer', 'Winter', 'Spring', 'Fall'])
            die4 = Die.Die(['House', 'Mountain'])
            dice_set = DiceSet.DiceSet([die1, die2, die3, die4], "theme1")
            dice_set2 = DiceSet.DiceSet([die1, die2, die3, die4], "theme2")
            store_dice_set(dice_set)
            store_dice_set(dice_set2)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
