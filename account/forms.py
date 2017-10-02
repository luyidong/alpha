#!/usr/bin/env python
#coding=utf-8
__author__ = "yidong.lu"
__email__ = "yidongsky@gmail.com"

from django import forms
from django.conf import  settings

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from account.models import Profile

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

User=get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self,*args,**kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        # user_qs = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        #     user = user_qs.first()
        if username and password:
            user = authenticate(username=username,password=password)
            if not user:
                raise forms.ValidationError("用户不存在")
            if not user.check_password(password):
                raise forms.ValidationError("密码无效")
            if not user.is_active:
                raise forms.ValidationError("用户不可用")
        return super(UserLoginForm,self).clean(*args,**kwargs)

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput,
        max_length=30,
        required=True,
        help_text='Usernames may contain <strong>alphanumeric</strong>, <strong>_</strong> and <strong>.</strong> characters')  # noqa: E501
    email = forms.CharField(
        widget=forms.EmailInput,
        required=True,
        max_length=75)

    password = forms.CharField(widget=forms.PasswordInput,label='password')
    password2 = forms.CharField(widget=forms.PasswordInput,required=True,label='Repeat  password')

    class Meta:
        model = User
        fields =[
            'username',
            'email',
            'password',
            'password2',

        ]
    def clean(self,*args,**kwargs):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("Passwords don\'t match.")
        return super(UserRegistrationForm,self).clean(*args,**kwargs)



class EmailBaseMixin(object):
    def clean_email(self):
        email = self.cleaned_data['email']
        if settings.ST_CASE_INSENSITIVE_EMAILS:
            email = email.lower()
        if not settings.ST_UNIQUE_EMAILS:
            return email
        is_taken = User.objects.filter(email=email).exists()
        if is_taken:
            raise forms.ValidationError(_("邮箱地址已经存在"))
        return  email
    def get_email(self):
        return self.cleaned_data["email"]

class EmailCheckForm(EmailBaseMixin,forms.Form):
    email = forms.CharField(label=_("email"),widget=forms.EmailInput,max_length=254)

class EmailChangeForm(EmailBaseMixin,forms.Form):
    email = forms.CharField(label=_("email"),widget=forms.EmailInput,max_length=254)
    password = forms.CharField(label=_("password"),widget=forms.PasswordInput)

    def __init__(self,user=None,*args,**kwargs):
        self.user = user
        super(EmailChangeForm,self).__init__(*args,**kwargs)

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not self.user.check_password(password):
            raise forms.ValidationError(_("密码输入错误"))

        return password


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name','last_name',)

class ProfileEditForm(forms.ModelForm):
    date_of_birth= forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = Profile
        fields = ('email','gender','date_of_birth','bio','url','company','location',)

    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         super(ProfileEditForm, self).__init__(*args, **kwargs)
         # self.fields['group'].queryset=Group.objects.filter(user=self.user)
         self.fields['email'].label = _(u'邮箱')
         self.fields['email'].widget.attrs["readonly"]= True
         # self.fields['email'].widget.attrs["disabled"]= True


