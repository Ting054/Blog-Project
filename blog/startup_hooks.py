import os
from blog.tasks import sync_db_to_redis_task

def call_startup_tasks():
    # 避免在 celery worker 中执行
    if os.environ.get('RUN_MAIN') == 'true' and 'celery' not in os.sys.argv:
        sync_db_to_redis_task.delay()