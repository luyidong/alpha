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
ajax_get_languages_for_category,
)

urlpatterns = [
    url(r'^index/$', index, name='post-index'),
    url(r'^create/$', create, name='post-create'),
    url(r'^(?P<slug>[\w-]+)/$', detail, name='post-detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', update, name='post-update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', delete, name='post-delete'),
    url(r'^comment/(?P<id>\d+)/$', comment_thread, name='comment-thread'),
    url(r'^comment/(?P<id>\d+)/delete/$', comment_delete,name='comment-delete'),
    url(r'^category/$', ajax_get_languages_for_category, name='category'),
    url(r'^topic/(?P<topic>[\w-]+)/$', topic, name='topic'),

]



