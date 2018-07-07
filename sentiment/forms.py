from django import forms
from .models import Feedback

class FeedbackForm(forms.Form):
	feedback = forms.CharField(label = 'feedback', max_length=2000)
	
