from django.db import models
from account.models import Account
from django import forms

# Create your models here.

class ContentManagement(models.Model):
	author = models.ForeignKey(Account, on_delete=models.CASCADE,)
	title = models.CharField(max_length = 50)
	body = models.CharField(max_length=300)
	summary = models.CharField(max_length=60)
	file_upload = models.FileField(upload_to='media')
	categories = models.CharField(max_length=70)

	REQUIRED_FIELDS = ['title','body','summary','file_upload']

	class Meta:
		db_table = "contentmanagement"

	# def __str__(self):
	# 	return self.title
