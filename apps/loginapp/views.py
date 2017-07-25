from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
# Create your views here.
def index(request):
    return render(request, "loginapp/index.html")
def register(request):
    result = User.objects.register(request.POST)
    if result['status'] == False:
        for error in result['error']:
            messages.error(request,error)
    else:
        messages.success(request,"User created")
    return redirect(reverse("loginapp:index"))
def login(request):
    result = User.objects.login(request.POST, request.session)
    if result == True:
        return redirect("friendapp:index")
    else:
        messages.error(request,"login failed")
        return redirect(reverse("loginapp:index"))