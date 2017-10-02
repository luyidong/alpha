#!/usr/bin/env python
#coding=utf-8
__author__ = "yidong.lu"
__email__ = "yidongsky@gmail.com"

from django import forms

from posts.models import Post,Category,TaggedItem
from pagedown.widgets import PagedownWidget


class CategoryForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = Category
        fields=[
            "name"
        ]

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    status = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "status",
        ]

class TaggedItemForm(forms.ModelForm):
    class Meta:
        model = TaggedItem
        fields = [
            "tag",
        ]


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    #parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea)
