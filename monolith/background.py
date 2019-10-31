from celery import Celery
from monolith.database import db, User, Story

BACKEND = BROKER = 'amqp://localhost'
celery = Celery(__name__, backend=BACKEND, broker=BROKER)

_APP = None


@celery.task
def fetch_all_runs():
    global _APP
    # lazy init
    if _APP is None:
        from monolith.app import create_app
        app = create_app()
        db.init_app(app)
    else:
        app = _APP
    return 1#runs_fetched
    
@celery.task
def init_db_context():
    global _APP
    # lazy init
    if _APP is None:
        from monolith.app import create_app
        app = create_app()
        db.init_app(app)
        _APP = app
    else:
        app = _APP
    return 1#runs_fetched
    
@celery.task
def async_like(story_id):
    with _APP.app_context():    
        story = Story.query.filter_by(id=story_id).first()
        story.likes += 1;
        db.session.commit()
        return 1
    
@celery.task
def async_dislike(story_id):
    with _APP.app_context(): 
        story = Story.query.filter_by(id=story_id).first()
        story.dislikes += 1;
        db.session.commit()
        return 1
    
@celery.task
def async_remove_like(story_id):
    with _APP.app_context(): 
        story = Story.query.filter_by(id=story_id).first()
        story.likes -= 1;
        db.session.commit()
        return 1
    
@celery.task  
def async_remove_dislike(story_id):
    with _APP.app_context(): 
        story = Story.query.filter_by(id=story_id).first()
        story.dislikes -= 1;
        db.session.commit()
        return 1

