from flask import Blueprint, redirect, render_template, request, abort
from monolith.database import db, Story, Like, Dislike
from monolith.auth import admin_required, current_user
from flask_login import (current_user, login_user, logout_user,
                         login_required)
from  sqlalchemy.sql.expression import func

stories = Blueprint('stories', __name__)

@stories.route('/')
def _stories(message=''):
    if current_user.is_anonymous:
        return redirect("/login", code=302)
    allstories = db.session.query(Story)
    return render_template("stories.html", message=message, stories=allstories,
                            url="/story/")

@stories.route('/story/<int:story_id>')
@login_required
def _story(story_id, message=''):
    story = Story.query.filter_by(id=story_id).first()
    if story is None:
        message = 'Story not found'
    return render_template("story.html", message=message, story=story,
                           url="/story/")

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
                           url="/story/")

@stories.route('/story/<int:story_id>/like')
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
    return _story(story_id, message)

@stories.route('/story/<int:story_id>/dislike')
@login_required
def _dislike(story_id):
    story = Story.query.filter_by(id=story_id).first()
    if story is None:
        abort(404)

    q = Dislike.query.filter_by(disliker_id=current_user.id, story_id=story_id)
    if q.first() is None:
        new_dislike = Dislike()
        new_dislike.disliker_id = current_user.id
        new_dislike.story_id = story_id
        # remove like, if present
        l = Like.query.filter_by(liker_id=current_user.id, story_id=story_id).first()
        if l is not None:
            db.session.delete(l)
        db.session.add(new_dislike)
        db.session.commit()
        message = 'Dislike added!'
    else:
        message = 'You\'ve already disliked this story!'
    return _story(story_id, message)

@stories.route('/story/<int:story_id>/remove_like')
@login_required
def _remove_like(story_id):
    l = Like.query.filter_by(liker_id=current_user.id, story_id=story_id).first()
    if l is None:
        message = 'You have to like it first!'
    else:
        db.session.delete(l)
        db.session.commit()
        message = 'You removed your like'
    return _story(story_id, message)
    
    
@stories.route('/story/<int:story_id>/remove_dislike')
@login_required
def _remove_dislike(story_id):
    d = Dislike.query.filter_by(disliker_id=current_user.id, story_id=story_id).first()
    if d is None:
        message = 'You didn\'t dislike it yet..'
    else:
        db.session.delete(d)
        db.session.commit()
        message = 'You removed your dislike!'
    return _story(story_id, message)
    
    
    
