from django.db import models
from model_utils import Choices
from django.contrib.auth.models import AbstractBaseUser, UserManager

# Create your models here.
class User(AbstractBaseUser):
	username = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	GENDER = Choices(
		('laki-laki','Laki-Laki'),
		('perempuan','Perempuan')
		)
	gender = models.CharField(choices=GENDER, max_length=50)
	email = models.CharField(max_length=50)
	address = models.CharField(max_length=100)
	USERNAME_FIELD = "username"

	objects = UserManager()