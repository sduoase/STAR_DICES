from flask_login import current_user
from flask import current_app
from monolith.database import db, User, Story
from monolith import celeryApp
from celery import shared_task

celery = celeryApp.celery
    
# Takes the story_id and and a boolean value defining whether or not it has to also decrement dislikes
@shared_task
def async_like(story_id, dislike_present=False):
    if current_app.config['TESTING']:
        (current_user.id)
    try:
        story = db.session.query(Story).filter_by(id=story_id).first()
    except: # pragma: no cover
        return -1
    story.likes += 1
    if dislike_present:
        story.dislikes -= 1
    db.session.commit()
    if current_app.config['TESTING']:
        (current_user.id)
    return 1

# Takes the story_id and and a boolean value defining whether or not it has to also decrement likes
@shared_task
def async_dislike(story_id, like_present=False):
    if current_app.config['TESTING']:
        (current_user.id)
    try:
        story = db.session.query(Story).filter_by(id=story_id).first()
    except: # pragma: no cover
        return -1
    story.dislikes += 1
    if like_present:
        story.likes -= 1
    db.session.commit()
    if current_app.config['TESTING']:
        (current_user.id)
    return 1
    
@shared_task
def async_remove_like(story_id):
    if current_app.config['TESTING']:
        (current_user.id)
    try:
        story = db.session.query(Story).filter_by(id=story_id).first()
    except: # pragma: no cover
        return -1
    story.likes -= 1
    db.session.commit()
    if current_app.config['TESTING']:
        (current_user.id)
    return 1
    
@shared_task 
def async_remove_dislike(story_id):
    if current_app.config['TESTING']:
        (current_user.id)
    try:
        story = db.session.query(Story).filter_by(id=story_id).first()
    except: # pragma: no cover
        return -1
    story.dislikes -= 1
    db.session.commit()
    if current_app.config['TESTING']:
        (current_user.id)
    return 1

