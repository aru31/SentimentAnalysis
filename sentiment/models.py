from django.db import models

# Create your models here.

class Feedback(models.Model):
	feedback = models.CharField(max_length = 2000)
