from monolith.app import create_app
from monolith import celeryApp

app = create_app()
celery = celeryApp.make_celery(app)
celeryApp.celery = celery


