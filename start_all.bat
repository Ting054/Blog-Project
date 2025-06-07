@echo off
setlocal

REM ===== 设置窗口标题和颜色 =====
title Start Typeidea Django + Celery + Redis
color 0A

REM ===== 启动 Redis（根据你的 Redis 安装路径修改） =====
start "Redis Server" cmd /k "C:\applicationss\Redis\redis-server"

REM ===== 启动 Django 项目 =====
start "Django Server" cmd /k "python manage.py runserver"

REM ===== 启动 Celery Worker =====
start "Celery Worker" cmd /k "C:\applicationss\Anaconda\envs\py310\Scripts\celery -A typeidea worker -l info"

REM ===== 启动 Celery Beat（定时任务） =====
start "Celery Beat" cmd /k "C:\applicationss\Anaconda\envs\py310\Scripts\celery -A typeidea beat -l info"

echo All services are starting in separate windows...
pause
endlocal
