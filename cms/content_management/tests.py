from django.test import TestCase
from content_management.models import ContentManagement
from account.models import Account
from django.urls import reverse
from rest_framework import status
import json
from django.contrib.auth.hashers import make_password
from django.http import QueryDict
# Create your tests here.


class ContentManagementTestCase(TestCase):

	def setUp(self):
		# import pdb;pdb.set_trace()
		password = make_password('Sarvesh12')
		self.account = Account.objects.create(email="sarvesh32@gmail.com", 
        	first_name="Sarvesh", last_name='Singh', address='Roopena',
        	city='Bangalore', state='Karnataka', country='India',
        	phone='+918896052348',password=password,pincode=564433)
		self.content = ContentManagement.objects.create(author_id=self.account.pk, 
			title='abc', body='xyz',summary='dhh', categories='sport',
			file_upload='/media/resume.pdf')
	

	def test_create_content(self):
		url = reverse('content management')
		login_url = reverse('login')
		# import pdb;pdb.set_trace()
		data = {'email':'sarvesh32@gmail.com','password':'Sarvesh12'}
		response = self.client.post(login_url, data, 
			content_type='application/json')
		response = json.loads(response.content)
		token = response['token']
		headers = {"Authorization": "Bearer %s" %token, "content_type":"multipart/form-data"}
		files=(('auther', (self.account.pk)),('title', ('mtv')),
			('body', ('eeee')),('summary', ('eeee')),('categories', ('eeee')),
			('file_upload',open('/home/dell/Downloads/resume.pdf','r')))
		data = {"title":"mtv","body":"sssss",
		"summary":"dddd","categories":"tv","file_upload":"resume.pdf"}
		query_dict = QueryDict('', mutable=True)
		query_dict.update(data)
		response = self.client.post(url, data=query_dict, headers=headers)

	def test_get_content(self):
		url = reverse('content management')
		login_url = reverse('login')
		# import pdb;pdb.set_trace()
		data = {'email':'sarvesh32@gmail.com','password':'Sarvesh12'}
		response = self.client.post(login_url, data, 
			content_type='application/json')
		response = json.loads(response.content)
		token = response['token']
		headers = {"Authorization": "Bearer %s" %token}
		response = self.client.get(url, headers=headers)
		# print(response.content)
		# self.assertEqual(response.status_code, status.HTTP_200_OK)
		response = self.client.get(url, headers=headers)
		self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

	def test_delete_content(self):
		url = reverse('content management')
		login_url = reverse('login')
		data = {'email':'sarvesh32@gmail.com','password':'Sarvesh12'}
		response = self.client.post(login_url, data, 
			content_type='application/json')
		response = json.loads(response.content)
		token = response['token']
		headers = {"Authorization": "Bearer %s" %token}
		data = {"id":1}
		response = self.client.delete(url, data=json.dumps(data), headers=headers)
		# print(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		response = self.client.delete(url, data=data, headers=headers)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		# import pdb;pdb.set_trace()
		# print(response)
	def test_update_content(self):
		url = reverse('content management')
		login_url = reverse('login')
		data = {'email':'sarvesh32@gmail.com','password':'Sarvesh12'}
		response = self.client.post(login_url, data, 
			content_type='application/json')
		response = json.loads(response.content)
		token = response['token']
		headers = {"Authorization": "Bearer %s" %token}
		data = {"id":1,'title':'sport'}
		response = self.client.put(url, data=json.dumps(data), headers=headers)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
