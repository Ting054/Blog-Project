from django.contrib import admin
from django.urls import path

from config.views import links
from .custom_site import custom_site
from blog.views import IndexView, CategoryView, TagView, PostDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category-list'),
    path('tag/<int:tag_id>/', TagView.as_view(), name='tag-list'),
    path('post/<int:post_id>/', PostDetailView.as_view(), name='post-detail'),
    path('links/', links, name='links'),

    path('super_admin/', admin.site.urls, name='super-admin'),
    path('admin/', custom_site.urls, name='admin'),
]