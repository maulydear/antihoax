from django.urls import path

from .import views

app_name='news'
urlpatterns = [
	path('', views.index, name='index'),
	path('new', views.news_upload, name='news_upload'),
	path('detail/<int:pk>', views.news_detail, name='news_detail'),
	path('update/<int:pk>', views.news_update, name='news_update'),
	path('history/<int:pk>', views.news_history, name='news_history'),
	path('delete/<int:pk>', views.news_delete, name='news_delete'),
	path('<int:pk>/agreement/', views.agreement, name='agreement'),
	path('agree', views.agree, name='agree'),
	path('disagree', views.disagree, name='disagree'),
	
]

