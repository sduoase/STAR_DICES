# encoding: utf8
import datetime as dt
import enum
import json
import random

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from monolith.classes import Die, DiceSet


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), unique=True, nullable=False)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    password = db.Column(db.Unicode(128))
    dateofbirth = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_anonymous = False

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self._authenticated = False

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

    def get_id(self):
        return self.id


class Story(db.Model):
    __tablename__ = 'story'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text(1000))  # around 200 (English) words
    date = db.Column(db.DateTime)
    # will store the number of likes, periodically updated in background
    likes = db.Column(db.Integer)
    rolls_outcome = db.Column(db.Unicode(1000))
    theme = db.Column(db.Unicode(128))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    dice_set_id = db.Column(db.Integer, db.ForeignKey('dice.id'))
    published = db.Column(db.Boolean, default=False)
    # define foreign key
    author = relationship('User', foreign_keys='Story.author_id')
    dice_set = relationship('Dice', foreign_keys='Story.dice_set_id')

    # TODO complete this method invocation about throw die button

    def __init__(self, *args, **kw):
        super(Story, self).__init__(*args, **kw)
        self.date = dt.datetime.now()

    def setText(self, text):
        self.text = text


class Like(db.Model):
    __tablename__ = 'like'

    liker_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), primary_key=True)
    liker = relationship('User', foreign_keys='Like.liker_id')

    story_id = db.Column(db.Integer, db.ForeignKey(
        'story.id'), primary_key=True)
    author = relationship('Story', foreign_keys='Like.story_id')

    liked_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'))  # TODO: duplicated ?
    liker = relationship('User', foreign_keys='Like.liker_id')

    # True iff it has been counted in Story.likes
    marked = db.Column(db.Boolean, default=False)


class Follow(db.Model):
    __tablename__ = 'follow'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followee = relationship('User', foreign_keys='Follow.user_id')

    followed_by_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), primary_key=True)
    follower = relationship('User', foreign_keys='Follow.user_id')

    def __init__(self, user, follower, *args, **kw):
        self.user_id = user
        self.followed_by_id = follower


class Dice(db.Model):
    __tablename__ = 'dice'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serialized_dice_set = db.Column(db.Unicode(1000), nullable=False)
    theme = db.Column(db.Unicode(128))


def _deserialize_dice_set(json_dice_set):
    dice_set = json.loads(json_dice_set)
    test = DiceSet.DiceSet([Die.Die(dice) for dice in dice_set], "test_theme")
    return test

# At the moment we handle only 1 dice set. In the future more will be available.


def retrieve_dice_set():
    dice = db.session.query(Dice).first()
    if dice is None:
        return None

    json_dice_set = dice.serialized_dice_set
    dice_set = _deserialize_dice_set(json_dice_set)
    dice_set.theme = dice.theme
    return dice_set


def store_dice_set(dice_set):
    db_entry = Dice()
    db_entry.theme = dice_set.theme
    db_entry.serialized_dice_set = json.dumps(dice_set.serialize())
    db.session.add(db_entry)
    db.session.commit()

def isFollowing(who, by_who):
    return db.session.query(Follow).filter(Follow.followed_by_id == by_who).filter(Follow.user_id == who).count() > 0

def retrieve_dice_bytheme():
    themes = []
    for row in db.session.query(Dice.theme.label('theme')).all():
        themes.append(row.theme)

    return themes
