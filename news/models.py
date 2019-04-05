from django.db import models
from model_utils import Choices
from django.urls import reverse
import datetime

# Create your models here.
class News(models.Model):
	title = models.CharField(max_length=60)
	desc = models.TextField(max_length=800)
	image = models.ImageField(upload_to='image/',blank=True)
	CATEGORY = Choices(
		('sport','Sport'),
		('politics','Politics'),
		('entertainment','Entertainment')
		)
	category = models.CharField(choices=CATEGORY, max_length=50)
	url = models.URLField(blank=True)
	user = models.ForeignKey('user.User',on_delete=models.CASCADE)
	date = models.DateField(("Date"), default=datetime.date.today)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('news_update', kwargs={'pk': self.pk})