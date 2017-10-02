#!/usr/bin/env python
#coding=utf-8
__author__ = "yidong.lu"
__email__ = "yidongsky@gmail.com"


from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from account.models import Profile
from django.contrib.auth.forms import PasswordChangeForm
from .utils.email import send_email_change_email
from .utils.tokens import UserEmailChangeTokenGenerator

from django.conf import settings as django_settings
import os
import json
from PIL import Image

from account.forms import (
    UserRegistrationForm,
    UserLoginForm,
    EmailCheckForm,
    EmailChangeForm,
    UserEditForm,
    ProfileEditForm
)

def index(request):
    templates='index.html'
    return  render(request,templates)

def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username,password=password)
        login(request,user)

        check = Profile.objects.filter(user=user)
        exists=check.exists()

        if exists:
            pass
        else:
            profile_create = Profile.objects.create(user=user)
        # if next:
        #     return  redirect(next)
        return redirect("/account")
        #print(request.user.is_authenticated())

    return render(request,"account/form.html",{"form":form,"title":title})

def logout_view(request):
    title = "Logout"
    logout(request)
    return render(request,"account/form.html",{"title":title})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST or None)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            user= user_form.cleaned_data.get('password')
            print user
            new_user.set_password(user_form.cleaned_data.get('password'))
            new_user.save()
            # new_user = authenticate(username=new_user.username,password=password)

            # profile = Profile.objects.create(user=new_user)

            return render(request,
                          'account/register_done.html',
                          {'new_user':new_user})
        else:
            print 'error'
    else:
        user_form = UserRegistrationForm()

    return render(request,'account/register.html',{'user_form':user_form})

# def profile

def settings(request):
    user = getattr(request, 'user', None)
    if request.method == 'POST':
        user_form = UserEditForm(instance=user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=user,
                                       data=request.POST,
                                       files=request.FILES)
        if all([user_form.is_valid(),profile_form.is_valid()]):
            user_form.save()
            profile_form.save()
            #messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=user.profile)

    return render(request, 'account/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form})

def PasswordChangeView(request):
    user = getattr(request, 'user', None)
    if request.method == 'POST':
        form = PasswordChangeForm(user=user,data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            # messages.info(request, _("Your password has been changed!"))
            return redirect(reverse('account:settings'))
    else:
        form = PasswordChangeForm(user=user)
    context = {'form': form, }

    return render(request,'account/profile_password_change.html',context)

def EmailChangeView(request):
    user = getattr(request, 'user', None)
    if request.method == 'POST':
        form = EmailChangeForm(user=user,data=request.POST)

        if form.is_valid():
            send_email_change_email(request, request.user, form.get_email())
            #messages.info(request, _("We have sent you an email so you can confirm the change!"))
            return redirect(reverse('account:email-change'))
    else:
        form = EmailChangeForm()

    context = {'form': form, }

    return render(request, 'account/profile_email_change.html', context)

def EmailChangeConfirm(request,token):
    user = getattr(request, 'user', None)
    user_email_change = UserEmailChangeTokenGenerator()

    if user_email_change.is_valid(user, token):
        email = user_email_change.get_email()
        form = EmailCheckForm(data={'email': email, })

        if form.is_valid():
            user.email = form.get_email()
            to_update = Profile.objects.filter(user=user).update(email=user.email)
            print user.email
            user.save()
            # messages.info(request, _("Your email has been changed!"))
            return redirect(reverse('account:settings'))

    # messages.error(request, _("Sorry, we were not able to change your email."))
    return redirect(reverse('account:settings'))


def EmailChangeView(request):
    user = getattr(request, 'user', None)
    if request.method == 'POST':
        form = EmailChangeForm(user=user,data=request.POST)

        if form.is_valid():
            send_email_change_email(request, request.user, form.get_email())
            #messages.info(request, _("We have sent you an email so you can confirm the change!"))
            return redirect(reverse('account:email-change'))
    else:
        form = EmailChangeForm()

    context = {'form': form, }

    return render(request, 'account/profile_email_change.html', context)

def picture(request):
    uploaded_picture = False
    try:
        if request.GET.get('upload_picture') == 'uploaded':
            uploaded_picture = True

    except Exception:  # pragma: no cover
        pass

    return render(request, 'account/picture.html',
                  {'uploaded_picture': uploaded_picture})

def upload_picture(request):
    try:

        profile_pictures = django_settings.MEDIA_ROOT + '/profile_pictures/'
        print profile_pictures
        if not os.path.exists(profile_pictures):
            os.makedirs(profile_pictures)
        f = request.FILES['picture']
        filename = profile_pictures + request.user.username + '_tmp.jpg'
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        im = Image.open(filename)
        width, height = im.size
        print 'upload_picture',filename,width,height

        if width > 350:
            new_width = 350
            new_height = (height * 350) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)

        return redirect('/account/settings/picture/?upload_picture=uploaded')

    except Exception as e:
        return redirect('/account/settings/picture/')



def save_uploaded_picture(request):
    try:
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))
        w = int(request.POST.get('w'))
        h = int(request.POST.get('h'))
        print x,y,w,h,request.user.username
        tmp_filename = django_settings.MEDIA_ROOT + '/profile_pictures/' + request.user.username + '_tmp.jpg'
        print 'tmp_filename',tmp_filename
        filename = django_settings.MEDIA_ROOT + '/profile_pictures/' + request.user.username + '.jpg'
        print 'filename',filename
        im = Image.open(tmp_filename)
        print 'im',im
        cropped_im = im.crop((x, y, w+x, h+y))
        print 'cropped_im',cropped_im
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)

    except Exception:
        print 'err'
        pass

    return redirect('/account/settings/picture/')