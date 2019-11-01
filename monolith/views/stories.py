from flask import Blueprint, redirect, render_template, request
from monolith.database import db, Story, Like, retrieve_dice_set
from monolith.auth import admin_required, current_user
from flask_login import (current_user, login_user, logout_user,
                         login_required)
from monolith.forms import UserForm
from monolith.classes import Die, DiceSet
from sqlalchemy.sql.expression import func

stories = Blueprint('stories', __name__)


@stories.route('/')
def _stories(message=''):
    if current_user.is_anonymous:
        return redirect("/login", code=302)
    allstories = db.session.query(Story)
    return render_template("stories.html", message=message, stories=allstories)


@stories.route('/story/<story_id>')
@login_required
def _story(story_id, message=''):
    story = Story.query.filter_by(id=story_id).first()
    if story is None:
        message = 'Story not found'
    return render_template("story.html", message=message, story=story,
                           like_it_url="/stories/like/",
                           dislike_it_url="/stories/dislike/")


@stories.route('/random_story')
@login_required
def _random_story(message=''):
    story = Story.query.order_by(func.random()).first()
    if story is None:
        # Should not happen.
        message = 'Something went wrong'
    return render_template("story.html", message=message, story=story,
                           like_it_url="/stories/like/",
                           dislike_it_url="/stories/dislike/")


@stories.route('/stories/like/<authorid>/<storyid>')
@login_required
def _like(authorid, storyid):
    q = Like.query.filter_by(liker_id=current_user.id, story_id=storyid)
    if q.first() != None:
        new_like = Like()
        new_like.liker_id = current_user.id
        new_like.story_id = storyid
        new_like.liked_id = authorid
        db.session.add(new_like)
        db.session.commit()
        message = ''
    else:
        message = 'You\'ve already liked this story!'
    return _stories(message)

# TODO to complete
@stories.route('/stories/new_story', methods=['GET'])
@login_required
def new_stories():
    dice_set = retrieve_dice_set()
    themes = [dice_set.theme]

    return render_template("new_story.html", themes=themes)

# TODO to complete
@stories.route('/write_story', methods=['POST'])
@login_required
def write_story():
    dice_set = retrieve_dice_set()
    face_set = dice_set.throw()
    print(request.form)

    return render_template("/write_story.html", theme=request.form["theme"], outcome=face_set)
