#!/usr/bin/env python
#coding=utf-8
__author__ = "yidong.lu"
__email__ = "yidongsky@gmail.com"

from django.conf.urls import url

from posts.views import (
    index,
    detail,
    create,
    update,
    delete,
    comment_thread,
    comment_delete,
    topic,
    CategoryView,
    post_ranking,
    PostLikeRedirect,
    PostLikeToggle,
    PostLikeAPIToggle,
)

urlpatterns = [
    url(r'^index/$', index, name='post-index'),
    url(r'^create/$', create, name='post-create'),
    url(r'^ranking/$', post_ranking, name='post-create'),
    url(r'^(?P<slug>[\w-]+)/$', detail, name='post-detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', update, name='post-update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', delete, name='post-delete'),
    url(r'^comment/(?P<id>\d+)/$', comment_thread, name='comment-thread'),
    url(r'^comment/(?P<id>\d+)/delete/$', comment_delete,name='comment-delete'),
    url(r'^topic/(?P<topic>[\w-]+)/$', topic, name='topic'),
    url(r'^c/(?P<slug>[\w-]+)/$', CategoryView, name='post-category'),
    url(r'^(?P<slug>[\w-]+)/like/$', PostLikeToggle.as_view(), name='like-toggle'),
    url(r'^api/(?P<slug>[\w-]+)/like/$', PostLikeAPIToggle.as_view(), name='like-api-toggle'),
    url(r'^(?P<slug>[\w-]+)/like/$', PostLikeRedirect.as_view(), name='like'),
]



