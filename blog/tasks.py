from celery import shared_task
from django.conf import settings
import redis
from blog.models import Post


def get_redis_conn():
    return redis.StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True
    )


@shared_task
def sync_db_to_redis_task():
    """
    程序启动时调用，将数据库中的 PV/UV 数据写入 Redis。
    这里的 UV 用虚拟用户填充，实际项目中应使用真实用户ID。
    """
    r = get_redis_conn()
    for post in Post.objects.all():
        r.set(f"pv:{post.id}", post.pv or 0)
        # 这里模拟 UV 的用户集合
        key_uv = f"uv:{post.id}"
        r.delete(key_uv)  # 先清空 Redis 里该文章的 UV 集合
        for i in range(post.uv or 0):
            r.sadd(key_uv, f"fakeuser{i}")


@shared_task
def sync_pv_uv_to_db():
    """
    定时任务，将 Redis 中的 PV/UV 数据同步回数据库，确保持久化。
    """
    r = get_redis_conn()

    # 同步 PV
    for key in r.scan_iter("pv:*"):
        try:
            post_id = key.split(":")[1]
            count = int(r.get(key))
            Post.objects.filter(pk=post_id).update(pv=count)
        except Exception as e:
            print(f"Sync PV error: {e}")

    # 同步 UV
    for key in r.scan_iter("uv:*"):
        try:
            post_id = key.split(":")[1]
            count = r.scard(key)  # UV 是集合的元素数量
            Post.objects.filter(pk=post_id).update(uv=count)
        except Exception as e:
            print(f"Sync UV error: {e}")