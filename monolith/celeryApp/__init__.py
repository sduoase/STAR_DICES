from celery import Celery

celery = None

def make_celery(app):
    _BROKER = 'amqp://localhost'
    _BACKEND = 'amqp://localhost'
    celery = Celery(app, backend=_BACKEND, broker=_BROKER)
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

