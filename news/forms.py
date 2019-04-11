from django import forms
from news.models import News, Vote
from user.models import User
from django.conf import settings

class NewsForm(forms.ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	desc = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
	image = forms.ImageField()
	CATEGORY = (
		('sport','Sport'),
		('politics','Politics'),
		('entertainment','Entertainment')
		)
	category = forms.CharField(widget=forms.Select(choices=CATEGORY,attrs={'class': 'form-control'}))
	date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required = False)
	url = forms.URLField()

	class Meta:
		model = News
		fields = ['title','desc','image','category', 'url', 'date']

	def __init__(self, *args, **kwargs):
		self.user_id = kwargs.pop('user_id', None)
		super(NewsForm, self).__init__(*args, **kwargs)

	def save(self, *args, **kwargs):
		news = super(NewsForm, self).save(commit=False, *args, **kwargs)
		news.user_id = self.user_id.id
		news.save()
		return news


class NewsAgreement(forms.ModelForm):
	image = forms.ImageField()
	url = forms.URLField()
	TYPE = (
		('agree','Agree'),
		('disagree','Disagree'),
		)
	type = forms.CharField(widget=forms.Select(choices=TYPE))

	class Meta:
		model = Vote
		fields = ['image', 'url', 'type']

	def __init__(self, *args, **kwargs):
		self.news_id = kwargs.pop('news_id', None)
		self.user_id = kwargs.pop('user_id', None)
		super(NewsAgreement, self).__init__(*args, **kwargs)

	def save(self, *args, **kwargs):
		vote = super(NewsAgreement, self).save(commit=False, *args, **kwargs)
		vote.news_id = self.news_id
		vote.user_id = self.user_id
		vote.save()
		return vote
