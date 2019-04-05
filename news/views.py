from django.shortcuts import render
from django.urls import reverse
from .models import News
from .forms import NewsForm
from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse

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
	context = dict(
		newsdetail = news
	)

	return TemplateResponse(request,'web/news/news_detail.html', context)

def news_update(request, pk):
	news = get_object_or_404(News, pk=pk)
	form = NewsForm(request.POST or None, instances = news)
	if form.is_valid():
		obj= form.save(commit=False)
		obj.user=request.user
		obj.save()
		return redirect('news:index')
	else:
		print(form.errors, 'FORM ERROR')

	return TemplateResponse(request,'web/news/news_update.html')

def news_history(request, pk):
    news = News.objects.filter(user=pk)
    context = dict(
		newshistory = news
	)  
    return TemplateResponse(request,'web/news/news_history.html', context)

def news_delete(request, pk):
    news = get_object_or_404(News, pk=pk)    
    if request.method=='POST':
        news.delete()
        return redirect('news:index')
    return TemplateResponse(request,'web/news/news_history.html')
