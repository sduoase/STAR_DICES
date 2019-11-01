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
    return render_template("stories.html", message=message, stories=allstories,
                            url="/story/")


@stories.route('/story/<story_id>')
@login_required
def _story(story_id, message=''):
    story = Story.query.filter_by(id=story_id).first()
    if story is None:
        message = 'Story not found'
    return render_template("story.html", message=message, story=story,
                           url="/story/", current_user=current_user)

@stories.route('/story/<story_id>/delete')
@login_required
def _delete_story(story_id):
    story = Story.query.filter_by(id=story_id)
    if story.first() is None:
        abort(404)

    if story.first().author_id != current_user.id:
        abort(401)
    else:
        story.delete()
        db.session.commit()
        message = 'Story sucessfully deleted'
    return render_template("message.html", message=message)


@stories.route('/random_story')
@login_required
def _random_story(message=''):
    story = Story.query.order_by(func.random()).first()
    if story is None:
        # Should not happen.
        message = 'Something went wrong'
    return render_template("story.html", message=message, story=story,
                           url="/story/", current_user=current_user)


@stories.route('/stories/like/<authorid>/<storyid>')
@login_required
def _like(story_id):
    story = Story.query.filter_by(id=story_id).first()
    if story is None:
        abort(404)
    
    q = Like.query.filter_by(liker_id=current_user.id, story_id=story_id)
    if q.first() is None:
        new_like = Like()
        new_like.liker_id = current_user.id
        new_like.story_id = story_id
        # remove dislike, if present
        d = Dislike.query.filter_by(disliker_id=current_user.id, story_id=story_id).first()
        if d is not None: 
            db.session.delete(d)
        db.session.add(new_like)
        db.session.commit()
        message = 'Like added!'
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
