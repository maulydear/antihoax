from django.contrib import admin
from .models import News, Vote


# Register your models here.
admin.site.register(News)
admin.site.register(Vote)