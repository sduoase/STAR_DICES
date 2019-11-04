import datetime
import json
import os

from flask import Flask, jsonify

from monolith.database import db, User, Story, Dice, retrieve_dice_set, store_dice_set
from monolith.views import blueprints
from monolith.auth import login_manager
from monolith.classes import Die, DiceSet

def create_app():
    app = Flask(__name__)
    app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    app.config['SECRET_KEY'] = 'ANOTHER ONE'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storytellers.db'

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

        q = db.session.query(Story).filter(Story.id == 1)
        story = q.first()
        if story is None:
            example = Story()
            example.title= 'Test title'
            example.text = 'Trial story of example admin user :) but i want to add more words just to test that those will be cut out in the home'
            example.likes = 42
            example.dislikes = 5
            example.author_id = 1
            db.session.add(example)
            example = Story()
            example.title= 'Test title 2'
            example.text = 'Trial story 2 of example admin user :) but i want to add more words just to test that those will be cut out in the home'
            example.likes = 42
            example.dislikes = 5
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
            dice_set = DiceSet.DiceSet([die1, die2, die3, die4])
            store_dice_set(dice_set)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
