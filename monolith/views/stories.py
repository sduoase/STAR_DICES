import json
from flask import Blueprint, redirect, render_template, request
from monolith.database import db, Story, Like, retrieve_dice_set, retrieve_dice_bytheme
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
        d = Dislike.query.filter_by(
            disliker_id=current_user.id, story_id=story_id).first()
        if d is not None:
            db.session.delete(d)
        db.session.add(new_like)
        db.session.commit()
        message = 'Like added!'
    else:
        message = 'You\'ve already liked this story!'
    return _stories(message)


@stories.route('/stories/new_story', methods=['GET', 'POST'])
@login_required
def new_stories():
    if request.method == 'GET':
        dice_themes = retrieve_dice_bytheme()
        return render_template("new_story.html", themes=dice_themes)
    else:
        stry = Story.query.filter(Story.author_id == current_user.id).filter(
            Story.published == 0).filter(Story.theme == request.form["theme"]).first()
        if stry != None:
            return redirect("../write_story/"+str(stry.id), code=302)

        dice_set = retrieve_dice_set(request.form["theme"])
        face_set = dice_set.throw()
        new_story = Story()
        new_story.author_id = current_user.id
        new_story.theme = request.form["theme"]
        new_story.rolls_outcome = json.dumps(face_set)
        db.session.add(new_story)
        db.session.flush()
        db.session.commit()
        db.session.refresh(new_story)
        return redirect('/write_story/'+str(new_story.id), code=302)


@stories.route('/write_story/<story_id>', methods=['POST', 'GET'])
@login_required
def write_story(story_id):
    story = Story.query.get(story_id)

    # NOTE If the story is already published i cannot edit nor republish!
    if story.published == 1:
        return redirect("../story/"+str(story.id), code=302)

    if request.method == 'POST':
        story.text = request.form["text"]
        story.title = request.form["title"]
        story.published = 1 if request.form["store_story"] == "1" else 0
        db.session.commit()

        if story.published == 1:
            return redirect("../story/"+str(story.id), code=302)

    return render_template("/write_story.html", theme=story.theme, outcome=story.rolls_outcome, title=story.title, text=story.text)
