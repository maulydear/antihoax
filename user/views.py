from django.shortcuts import render, redirect, get_object_or_404
from user.forms import UserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from news.models import News
from django.template.response import TemplateResponse
from django.db.models import Count
from django.core.exceptions import PermissionDenied


def index(request):
    news = News.objects.all()
    newslimit = News.objects.all().order_by('-id')[:3]
    search = request.GET.get('s', False)
    category = request.GET.get('category', False)
    politics = request.GET.get('politics', False)
    entertainment = request.GET.get('entertainment', False)

    if category:
        news = News.objects.filter(category=category)

    if politics:
        news = News.objects.filter(politics=politics)

    if entertainment:
        news = News.objects.filter(entertainment=entertainment)
        
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

def charts(request):
    context={}

    list_pol=[]
    list_spo=[]
    list_ent=[]

    news = News.objects.filter(category='politics').values('date').annotate(total=Count('date'))
    for new in news:
        date = (
           (new["date"].strftime("%m")))
        list_pol.append([date, new["total"]])

    news = News.objects.filter(category='sport').values('date').annotate(total=Count('date'))
    for new in news:
        date = (
           (new["date"].strftime("%m")))
        list_spo.append([date, new["total"]])

    news = News.objects.filter(category='entertainment').values('date').annotate(total=Count('date'))
    for new in news:
        date = (
           (new["date"].strftime("%m")))
        list_ent.append([date, new["total"]])

    context['politics']= list_pol
    context['sport']= list_spo
    context['entertainment']= list_ent
        
    return TemplateResponse(request, 'web/adm/charts.html', context)

# def chartss(request):
#     dataset = News.objects.values(category).annotate(pol_count=Count('category', filter(pol=True)), 
#                                                     spo_count=Count('category', filter(spo=True)), 
#                                                     ent_count=Count('category', filter(ent=True))
#         )

#     categories = list()
#     pol_data= list()
#     spo_data= list()
#     ent_data= list()

#     for entry in dataset:
#         categories.append('% Cat' % entry['category'])
#         pol_data.append(entry['pol_count'])
#         spo_data.append(entry['spo_count'])
#         ent_data.append(entry['ent_count'])

#     pol_series={
#         'name' : 'Politics',
#         'data' : pol_data,
#         'color' : 'blue'
#     }

#     spo_series={
#         'name' : 'Sport',
#         'data' : spo_data,
#         'color' : 'red'
#     }

#     ent_series={
#         'name' : 'Entertainment',
#         'data' : ent_data,
#         'color' : 'green'
#     }

#     chart = {
#         'chart': {'type' : 'column'},
#         'title' : {'text': 'Uploaded Hoax'},
#         'xAxis' : {'categories' : categories},
#         'series' : [pol_series, spo_series, ent_series]
#     }

#     dump = json.dumps(chart)

#     return render(request, 'charts.html', {'chart' : dump})


def indexadm(request):
    news = News.objects.all()
    search = request.GET.get('s', False)
    category = request.GET.get('category', False)
    politics = request.GET.get('politics', False)
    entertainment = request.GET.get('entertainment', False)

    if category:
        news = News.objects.filter(category=category)

    if politics:
        news = News.objects.filter(politics=politics)

    if entertainment:
        news = News.objects.filter(entertainment=entertainment)

    if search:
        news = News.objects.filter(title=search)

    context = dict(
        news = news.order_by('-id')

    )
    return TemplateResponse(request,'web/adm/index.html',context)

def adm_deletenews(request, pk, template_name='web/adm/adm_confirm_delete.html'):
    news = get_object_or_404(News, pk=pk)    
    if request.method=='POST':
        news.delete()
        return redirect('user:indexadm')
    return render(request, template_name, {'n':news})

def adm_login(request):
    authentication = LoginForm(data=request.POST or None)

    if request.method == 'POST': 
        if authentication.is_valid():
            login(request, authentication.get_user())
            user = authentication.get_user()

            if user.is_superuser:
                return HttpResponseRedirect(reverse('user:indexadm'))
                
        else:
            print(authentication.errors)
            return HttpResponse("Invalid login details given")

    context=dict(
        auth = authentication
        )

    return render(request, 'web/adm/login.html', context)

def adm_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user:adm_login'))
