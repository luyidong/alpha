#!/usr/bin/env python
#coding=utf-8
#__author__  = louis,
# __date__   = 2017-06-06 23:18,
#  __email__ = yidongsky@gmail.com,
#   __name__ = urlify.py


from urllib import quote_plus
from django import template

register = template.Library()

@register.filter
def urlify(value):
    return quote_plus(value)