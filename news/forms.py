from django import forms
from news.models import News
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
	user = forms.ModelChoiceField(queryset=User.objects.all())
	date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required = False)

	class Meta:
		model = News
		exclude = ()

	def __init__(self, *args, **kwargs):
		self.user_id = kwargs.pop('user_id', None)
		super(NewsForm, self).__init__(*args, **kwargs)