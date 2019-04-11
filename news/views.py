from django.urls import reverse
from .models import News, Vote
from .forms import NewsForm, NewsAgreement
from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

def index(request):
	newslimit = News.objects.all().order_by('-id')[:3]
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
		news = news.order_by('-id'),
		newslimit = newslimit

	)
	return TemplateResponse(request,'web/news/index.html',context)

@login_required
def news_upload(request):
    form = NewsForm(request.POST or None, request.FILES or None, user_id=request.user)
    context = dict(
		newsupload = form
	)
    if form.is_valid():
        form.save()
        return redirect('news:index')
    else:
    	print(form.errors, 'FORM ERROR')

    return TemplateResponse(request,'web/news/news_upload.html', context)

def news_detail(request, pk):
	news = get_object_or_404(News, pk=pk)
	agree = Vote.objects.filter(type='agree', news=pk).count()
	disagree = Vote.objects.filter(type='disagree', news=pk).count()
	context = dict(
		newsdetail = news,
		agree = agree,
		disagree = disagree
	)

	return TemplateResponse(request,'web/news/news_detail.html', context)

@login_required
def news_update(request, pk):
	news = get_object_or_404(News, pk=pk)
	form = NewsForm(request.POST or None, request.FILES or None, instance = news, user_id=request.user)
	context = dict(
		newsupdate = form
	)
	if form.is_valid():
		form.save()
		return redirect('news:index')
	else:
		print(form.errors, 'FORM ERROR')

	return TemplateResponse(request,'web/news/news_update.html', context)

@login_required
def news_delete(request, pk, template_name='web/news/news_confirm_delete.html'):
    news = get_object_or_404(News, pk=pk)    
    if request.method=='POST':
        news.delete()
        return redirect('news:index')
    return render(request, template_name, {'n':news})

@login_required
def news_history(request, pk):
	news = News.objects.filter(user=pk)
	print(news)
	context = dict(
		newshistory = news.order_by('-id')
	)
	return TemplateResponse(request,'web/news/news_history.html', context)

@login_required
def agreement(request, pk):
	form = NewsAgreement(request.POST or None, request.FILES or None, news_id=pk, user_id=request.user.id)
	vote = Vote.objects.filter(user_id=request.user.id)

	for n in vote:
		if pk == n.news.id:
			return TemplateResponse(request,'web/news/news_agreement.html', {'Status': 'Sorry, You can not vote twice... '})

	context = dict(
		newsagreement = form
	)

	if form.is_valid():
		form.save()
		return redirect('news:index')
	else:
		print(form.errors, 'FORM ERROR')

	return TemplateResponse(request,'web/news/news_agreement.html', context)

def agree(request):
	agree = Vote.objects.filter(type='agree')
	context = dict(
		agree = agree.order_by('-id')

	)
	return TemplateResponse(request,'web/news/news_agree.html',context)

def disagree(request):
	disagree = Vote.objects.filter(type='disagree')
	context = dict(
		disagree = disagree.order_by('-id')

	)
	return TemplateResponse(request,'web/news/news_disagree.html',context)