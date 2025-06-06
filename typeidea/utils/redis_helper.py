import redis
from django.conf import settings

# 单例 Redis 连接
r = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True  # 默认返回字符串
)

def incr_pv(post_id):
    key = f'pv:{post_id}'
    return r.incr(key)

def incr_uv(post_id, uid):
    key = f'uv:{post_id}:{uid}'
    if not r.exists(key):
        r.set(key, 1, ex=24 * 60 * 60)  # 24小时过期
        return True
    return False