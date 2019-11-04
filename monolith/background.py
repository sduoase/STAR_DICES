from monolith.database import db, User, Story
from monolith import celeryApp

celery = celeryApp.celery
    
@celery.task
def async_like(story_id):
    try:
        story = db.session.query(Story).filter_by(id=story_id).first()
    except:
        return -1
    story.likes += 1
    db.session.commit()
    return 1
        
@celery.task
def async_dislike(story_id):
    try:
        story = db.session.query(Story).filter_by(id=story_id).first()
    except:
        return -1
    story.dislikes += 1
    db.session.commit()
    return 1
    
@celery.task
def async_remove_like(story_id):
    try:
        story = db.session.query(Story).filter_by(id=story_id).first()
    except:
        return -1
    story.likes -= 1
    db.session.commit()
    return 1
    
@celery.task  
def async_remove_dislike(story_id):
    try:
        story = db.session.query(Story).filter_by(id=story_id).first()
    except:
        return -1
    story.dislikes -= 1
    db.session.commit()
    return 1

