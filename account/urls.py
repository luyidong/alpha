#!/usr/bin/env python
#coding=utf-8
__author__ = "yidong.lu"
__email__ = "yidongsky@gmail.com"

from django.conf.urls import url

from account.views import (
    index,
    register,
    login_view,
    logout_view,
    settings,
    PasswordChangeView,
    EmailChangeView,
    EmailChangeConfirm,
    picture,
    upload_picture,
    save_uploaded_picture,
)

urlpatterns = [
    # url(r'^login/$', views.user_login, name='login'),
    # url(r'^$', views.dashboard, name='dashboard'),
    url(r'^$', index, name='index'),

    url(r'^register/$', register, name='register'),
    #
    # login / logout urls
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$',logout_view,name='logout'),
    # url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    # url(r'^logout-then-login/$', 'django.contrib.auth.views.logout_then_login', name='logout_then_login'),

    url(r'^settings/$',settings,name='settings'),
    # change password urls
    url(r'^password-change/$', PasswordChangeView, name='password-change'),
    url(r'^email-change/$', EmailChangeView, name='email-change'),
    url(r'^email-change/(?P<token>[0-9A-Za-z_\-\.]+)/$', EmailChangeConfirm, name='email-change-confirm'),

    url(r'^settings/picture/$',picture, name='picture'),
    url(r'^settings/upload_picture/$', upload_picture,
        name='upload_picture'),
    url(r'^settings/save_uploaded_picture/$', save_uploaded_picture,
        name='save_uploaded_picture'),


    # url(r'^password-change/$', password_change, name='password_change'),
    # url(r'^password-change/done/$', password_change_done, name='password_change_done'),
    #
    # # restore password urls
    # url(r'^password-reset/$', password_reset, name='password_reset'),
    # url(r'^password-reset/done/$', password_reset_done, name='password_reset_done'),
    # # url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    # url(r'^password-reset/complete/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),

]



