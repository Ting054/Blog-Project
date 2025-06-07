import os
from celery import Celery

# 动态获取 profile（默认为 develop）
profile = os.environ.get('TYPEIDEA_PROFILE', 'develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'typeidea.settings.{profile}')

# 初始化 Celery 实例
app = Celery('typeidea')

# 加载 Django settings 中的 celery 配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现任务模块
app.autodiscover_tasks(['blog'])
