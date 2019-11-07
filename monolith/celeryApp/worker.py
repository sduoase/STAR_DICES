from monolith.app import create_app # pragma: no cover
from monolith import celeryApp # pragma: no cover

app = create_app() # pragma: no cover
celery = celeryApp.make_celery(app) # pragma: no cover
celeryApp.celery = celery # pragma: no cover

# this is a test comment

