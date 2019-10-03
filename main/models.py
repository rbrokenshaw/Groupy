

from django.db import models
from django.contrib.auth.models import User

class FileUpload(models.Model):
	csv_file = models.FileField(upload_to='uploads/%Y/%m/%d')

class Solutions(models.Model):
	csv_file = models.FileField(upload_to='solutions')

class SavedSolutions(models.Model):
	csv_file = models.FileField(upload_to='saved')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=100, default="solution.csv")
