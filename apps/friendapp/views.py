# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import User

# Create your views here.
def index(request):
    if 'id' not in request.session:
        return redirect(reverse('loginapp:index'))
    context = {
        "user": User.objects.get(id = request.session['id']),
        "users": User.objects.all().order_by("-created_at")[:3],
    }
    return render(request, "friendapp/index.html", context)
def logout(request):
    request.session.pop('id')
    return redirect(reverse("loginapp:index"))
def view(request):
    if 'id' not in request.session:
        return redirect(reverse('loginapp:index'))
    user = User.objects.get(id=request.session['id'])
    context = {
        "user": User.objects.get(id=request.session['id']),
        "friends": user.friends.all(),
        "count": user.friends.all().count()
    }
    return render(request, 'friendapp/view.html', context)
def add(request):
    if 'id' not in request.session:
        return redirect(reverse('loginapp:index'))
    user = User.objects.get(id = request.session['id'])
    others = User.objects.exclude(id=user.id)
    friends = user.friends.all()
    context = {
        "users": others.exclude(id__in=friends)
    }
    return render(request, 'friendapp/add.html', context)
def delete(request, user_id):
    user = User.objects.get(id = request.session['id'])
    user.friends.remove(User.objects.get(id = user_id))
    return redirect(reverse('friendapp:view'))
def addFriend(request, user_id):
    user = User.objects.get(id = request.session['id'])
    user.friends.add(User.objects.get(id = user_id))
    return redirect(reverse('friendapp:add'))