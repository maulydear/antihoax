from django.db import models
from model_utils import Choices
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin

# Create your models here.
class CustomUserManager(UserManager):

   def create_user(self, password, **extra_fields):
   		user = self.model(is_active=True, is_superuser=False,**extra_fields)
   		if password:
   			user.set_password(password)
   			user.save(using=self._db)

   		return user

   def create_superuser(self, username, password, **extra_fields):
   		user = self.create_user(username=username, password=password, **extra_fields)
   		user.is_staff = True
   		user.is_active = True
   		user.is_superuser = True
   		user.save(using=self._db)
   		return user

class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(max_length=50,unique=True,db_index=True)
	name = models.CharField(max_length=50)
	GENDER = Choices(
		('laki-laki','Laki-Laki'),
		('perempuan','Perempuan')
		)
	gender = models.CharField(choices=GENDER, max_length=50)
	email = models.EmailField(max_length=50,db_index=True,default=None,blank=True,null=True)
	address = models.CharField(max_length=100)
	USERNAME_FIELD = "username"
	REQUIRED_FIELDS=['email']

	is_active = models.BooleanField(
       'active', default=True, blank=True, null=True)
	is_staff = models.BooleanField(
       'staff status', default=False, blank=True, null=True)

	objects = CustomUserManager()
