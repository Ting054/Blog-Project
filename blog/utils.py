import redis
from django.conf import settings
from blog.models import Post

def sync_db_to_redis():
    r = redis.StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True
    )

    for post in Post.objects.all():
        r.set(f"pv:{post.id}", post.pv or 0)
        for _ in range(post.uv or 0):
            r.sadd(f"uv:{post.id}", f"fakeuser{_}")  # uv 没有唯一用户 ID，用虚拟数据填充