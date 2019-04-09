from django.shortcuts import render, redirect
from user.forms import UserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from news.models import News
from django.template.response import TemplateResponse


def index(request):
    news = News.objects.all()
    newslimit = News.objects.all().order_by('-id')[:3]
    search = request.GET.get('s', False)
    if search:
        news = News.objects.filter(title=search)

    context = dict(
        news = news.order_by('-id'),
        newslimit = newslimit

    )
    return TemplateResponse(request,'web/user/index.html',context)

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user:index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            return redirect(reverse('user:index'))
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'web/user/registration.html',
                          {'user_form':user_form,
                           'registered':registered})

def user_login(request):
    authentication = LoginForm(data=request.POST or None)
    if request.method == 'POST': 
        if authentication.is_valid():
            login(request, authentication.get_user())
            return HttpResponseRedirect(reverse('news:index'))
        else:
            print(authentication.errors)
            return HttpResponse("Invalid login details given")

    context=dict(
        auth = authentication
        )

    return render(request, 'web/user/login.html', context)