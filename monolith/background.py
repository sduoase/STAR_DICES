from flask_login import current_user
from flask import current_app
from monolith.database import db, User, Story
from monolith import celeryApp
from celery import shared_task

celery = celeryApp.celery
    
'''
Function used to add to the message queue a like
story_id is the id of the story to like
dislike_present represents whether or not to also remove a dislike
'''
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
'''
Function used to add to the message queue a dislike
story_id is the id of the story to like
dislike_present represents whether or not to also remove a like
'''
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

'''
Function used to add to the message queue a remove_like
story_id is the id of the story to remove the like from
'''  
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
    
'''
Function used to add to the message queue a remove_dislike
story_id is the id of the story to remove the dislike from
'''    
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

