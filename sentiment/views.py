from django.shortcuts import render, redirect
from .models import Feedback
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from .forms import FeedbackForm
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
import Features, EntitiesOptions, KeywordsOptions
import time
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def create(request):
	if request.method == "GET":
		form = FeedbackForm()
	elif request.method == "POST":
		form = FeedbackForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			feedback = Feedback(feedback = data.get('feedback'))
			feedback.save()
			return redirect('view', feedback.id)
	return render(request, 'sentiment/create.html', {'form': form})


def view(request, key):
	if Feedback.objects.filter(id = key).exists():
		feedback = Feedback.objects.get(id = key)
		net = 0
		tag = ""
		header = ""

		natural_language_understanding = NaturalLanguageUnderstandingV1(
			username='e624d94c-0e1d-449c-a0c3-4e6ba839918b',
			password='axlca4eonzhv',
			version='2018-03-16')

		response = natural_language_understanding.analyze(
			text=feedback.feedback,
			features=Features(
				entities=EntitiesOptions(
					emotion=True,
					sentiment=True,
					limit=2),
				keywords=KeywordsOptions(
					emotion=True,
					sentiment=True,
					limit=2)))
		for emo in response['keywords']:
			net = net + (emo['emotion']['sadness'] + emo['emotion']['fear'] + emo['emotion']['disgust'] + emo['emotion']['anger'])*0.25 - emo['emotion']['joy']

		if net >= 0.33 and net <= 0.55:
			tag = 'Urgent! Attention needed'
		elif net >= 0 and net < 0.33:
			tag = 'Complaint! Attention Required'
		elif net < 0:
			tag = 'Good Work! Keep it up'

		localtime = time.asctime( time.localtime(time.time()) ) + '\n'

		if tag == 'Urgent! Attention needed' or tag == 'Complaint! Attention Required':
			header = 'COMPLAINT! A Mail has been sent to the respective authorities, Patience would be highly appreciated' + '\n'
			subject = 'Complaint that need to be addressed immidiately'
			message = feedback.feedback
			from_email = settings.EMAIL_HOST_USER
			to_list = ['dmpgbsnl@gmail.com', settings.EMAIL_HOST_USER] ## SAMPLE TO BSNL ##
			send_mail(subject, message, from_email, to_list, fail_silently=True)
		if tag == 'Good Work! Keep it up':
			header = 'Thank You for your feedback, Always Happy to Help'


		return render(request, 'sentiment/view.html', {'key': key, 'feedback': feedback.feedback, 'response': response, 'net': net, 'tag': tag, 'header': header, 'localtime': localtime})
	else:
		raise Http404("Feedback Doesnot Exist")





