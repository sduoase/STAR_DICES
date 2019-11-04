from flask import Blueprint, redirect, render_template, request
from monolith.database import db, Story, Like, Dislike
from monolith.auth import admin_required, current_user
from flask_login import (current_user, login_user, logout_user,
                         login_required)
from sqlalchemy.sql.expression import func
from monolith.background import async_like, async_dislike, async_remove_like, async_remove_dislike

stories = Blueprint('stories', __name__)

@stories.route('/')
def _stories(message=''):
    #init_db_context.delay()
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
                           url="/story/")

@stories.route('/random_story')
@login_required
def _random_story(message=''):
    story = Story.query.order_by(func.random()).first()
    if story is None:
        # Should not happen.
        message = 'Something went wrong'
    return render_template("story.html", message=message, story=story,
                           url="/story/")

@stories.route('/story/<story_id>/like')
@login_required
def _like(story_id):
    q = Like.query.filter_by(liker_id=current_user.id, story_id=story_id)
    story = Story.query.filter_by(id=story_id).first()
    if q.first() == None:
        new_like = Like()
        new_like.liker_id = current_user.id
        new_like.story_id = story_id
        new_like.liked_id = story.author_id
        # remove dislike, if present
        d = Dislike.query.filter_by(disliker_id=current_user.id, story_id=story_id).first()
        if d is not None: 
            db.session.delete(d)
            async_remove_dislike.delay(story_id)
        async_like.delay(story_id)
        print(new_like)
        db.session.add(new_like)
        db.session.commit()
        message = 'Like added!'
    else:
        print('I?VE ALREADY LIKED THIS!')
        message = 'You\'ve already liked this story!'
    return _story(story_id, message)

@stories.route('/story/<story_id>/dislike')
@login_required
def _dislike(story_id):
    q = Dislike.query.filter_by(disliker_id=current_user.id, story_id=story_id)
    story = Story.query.filter_by(id=story_id).first()
    if q.first() == None:
        new_dislike = Dislike()
        new_dislike.disliker_id = current_user.id
        new_dislike.story_id = story_id
        new_dislike.disliked_id = story.author_id
        # remove like, if present
        l = Like.query.filter_by(liker_id=current_user.id, story_id=story_id).first()
        if l is not None:
            db.session.delete(l)
            async_remove_like.delay(story_id)
        async_dislike.delay(story_id)
        db.session.add(new_dislike)
        db.session.commit()
        message = 'Dislike added!'
    else:
        message = 'You\'ve already disliked this story!'
    return _story(story_id, message)

@stories.route('/story/<story_id>/remove_like')
@login_required
def _remove_like(story_id):
    l = Like.query.filter_by(liker_id=current_user.id, story_id=story_id).first()
    if l == None:
        message = 'You have to like it first!'
    else:
        async_remove_like.delay(story_id)
        db.session.delete(l)
        db.session.commit()
        message = 'You removed your like'
    return _story(story_id, message)
    
    
@stories.route('/story/<story_id>/remove_dislike')
@login_required
def _remove_dislike(story_id):
    d = Dislike.query.filter_by(disliker_id=current_user.id, story_id=story_id).first()
    if d == None:
        message = 'You didn\'t dislike it yet..'
    else:
        async_remove_dislike.delay(story_id)
        db.session.delete(d)
        db.session.commit()
        message = 'You removed your dislike!'
    return _story(story_id, message)
    
    
    
