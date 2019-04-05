from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user.views import index, special, user_logout, user_login
from news import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/',include('news.urls')),
    path('user/',include('user.urls')),
    path('special/',special, name='special'),
    path('logout/', user_logout, name='logout'),
    path('accounts/login/', user_login, name='user_login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
