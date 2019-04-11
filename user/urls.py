from django.urls import path

from .import views

app_name='user'
urlpatterns = [
	path('', views.index, name='index'),
	path('register/', views.register, name='register'),
	path('user_login/', views.user_login, name='user_login'),
	path('logout/', views.user_logout, name='user_logout'),
	path('charts/', views.charts, name='charts'),
	# path('chartss/', views.chartss, name='chartss'),
	path('indexadm/', views.indexadm, name='indexadm'),
	path('adm_deletenews/<int:pk>', views.adm_deletenews, name='adm_deletenews'),
	path('adm_logout/', views.adm_logout, name='adm_logout'),
	path('adm_login/', views.adm_login, name='adm_login'),
	
]

