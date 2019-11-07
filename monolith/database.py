# encoding: utf8
import datetime as dt
import enum
import json

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
    title= db.Column(db.Text(50))
    text = db.Column(db.Text(1000), nullable=True)  # around 200 (English) words
    rolls_outcome = db.Column(db.Unicode(1000))
    theme = db.Column(db.Unicode(128))
    date = db.Column(db.DateTime)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    published = db.Column(db.Boolean, default=False)
    # define foreign key 
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = relationship('User', foreign_keys='Story.author_id')

    def __init__(self, *args, **kw):
        super(Story, self).__init__(*args, **kw)
        self.date = dt.datetime.now()

class Like(db.Model):
    __tablename__ = 'like'
    
    liker_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    liker = relationship('User', foreign_keys='Like.liker_id')

    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), primary_key=True)
    author = relationship('Story', foreign_keys='Like.story_id')

    marked = db.Column(db.Boolean, default = False) # True iff it has been counted in Story.likes
    
class Dislike(db.Model):
    __tablename__ = 'dislike'
    
    disliker_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    disliker = relationship('User', foreign_keys='Dislike.disliker_id')

    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), primary_key=True)
    author = relationship('Story', foreign_keys='Dislike.story_id')

    marked = db.Column(db.Boolean, default = False) # True iff it has been counted in Story.likes 

class Follow(db.Model):
    __tablename__ = 'follow'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followee = relationship('User', foreign_keys='Follow.user_id')

    followed_by_id= db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    follower = relationship('User', foreign_keys='Follow.user_id')

    def __init__(self, user, follower, *args, **kw):
        self.user_id = user
        self.followed_by_id = follower


class Dice(db.Model):
    __tablename__ = 'dice_set'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serialized_dice_set = db.Column(db.Unicode(1000), nullable=False)
    theme = db.Column(db.Unicode(128))

def _deserialize_dice_set(json_dice_set, theme):
    dice_set = json.loads(json_dice_set)
    test = DiceSet.DiceSet([Die.Die(dice) for dice in dice_set], theme)
    return test

def retrieve_dice_set(theme=None):
    if theme == None:
        dice = db.session.query(Dice).first()
    else:
        dice = db.session.query(Dice).filter(Dice.theme==theme).first()
    if dice is None:
        return None

    json_dice_set = dice.serialized_dice_set
    dice_set = _deserialize_dice_set(json_dice_set, dice.theme)
    return dice_set

def retrieve_themes():
    themes = []
    for row in db.session.query(Dice.theme.label('theme')).all():
        themes.append(row.theme)

    return themes

def store_dice_set(dice_set):
    db_entry = Dice()
    db_entry.theme = dice_set.theme
    db_entry.serialized_dice_set = json.dumps(dice_set.serialize())
    db.session.add(db_entry)
    db.session.commit()

def isFollowing(who, by_who):
    return db.session.query(Follow).filter(Follow.followed_by_id == by_who).filter(Follow.user_id == who).count() > 0

def getStats(user_id):
    stories = db.session.query(Story).filter(Story.author_id == user_id)
    tot_stories=0
    tot_likes=0
    tot_dislikes=0
    for story in stories:
        tot_stories+=1
        tot_likes+=story.likes
        tot_dislikes+=story.dislikes
    if tot_stories==0:
        return 0
    if tot_likes==0:
        tot_likes=1
    if tot_dislikes==0:
        tot_dislikes=1
    return round((tot_likes/tot_dislikes)/tot_stories, 2)

def is_date(string):
    try: 
        dt.datetime.strptime(string, '%Y-%m-%d')
        return True

    except ValueError:
        return False

def get_suggested_stories(user_id):
    lastUsedThemes= [story.theme for story in db.session.query(Story).filter(Story.author_id == user_id).distinct()]
    likedStories= [like.story_id for like in db.session.query(Like).filter(Like.liker_id==user_id)]
    suggestedStories= (db.session.query(Story).filter(Story.author_id != user_id)
                                              .filter(Story.published==1)
                                              .order_by(Story.likes.desc())
                                              .all())
    suggestedStories = [story for story in suggestedStories if story.id not in likedStories]
    suggestedStories = [story for story in suggestedStories if story.theme in lastUsedThemes][:5]
    return suggestedStories
