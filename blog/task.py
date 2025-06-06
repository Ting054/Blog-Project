from celery import shared_task
from django.conf import settings
import redis
from blog.models import Post


@shared_task
def sync_pv_uv_to_db():
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, decode_responses=True)

    for key in r.scan_iter("pv:*"):
        try:
            post_id = key.split(":")[1]
            count = int(r.get(key))
            Post.objects.filter(pk=post_id).update(pv=count)
        except Exception as e:
            print(f"Sync PV error: {e}")

    for key in r.scan_iter("uv:*"):
        try:
            post_id = key.split(":")[1]
            count = int(r.scard(key))
            Post.objects.filter(pk=post_id).update(uv=count)
        except Exception as e:
            print(f"Sync UV error: {e}")
