from django.test import TestCase
from content_management.models import ContentManagement
from account.models import Account
from django.urls import reverse
from rest_framework import status
import json
from django.contrib.auth.hashers import make_password
from django.http import QueryDict
import requests
from requests.structures import CaseInsensitiveDict
from django.test import Client
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.test import APITestCase, RequestsClient

# Create your tests here.


class ContentManagementTestCase(APITestCase):

	def setUp(self):
		# import pdb;pdb.set_trace()
		self.client = Client()
		password = make_password('Sarvesh@123')
		self.account = Account.objects.create(email="sarveshsingh@gmail.com", 
        	first_name="Sarvesh", last_name='Singh', address='Roopena',
        	city='Bangalore', state='Karnataka', country='India',
        	phone='+918896052348',password=password,pincode=564433)
		self.content = ContentManagement.objects.create(
			author_id=self.account.pk, title='abc', body='xyz', 
			summary='dhh', categories='sport', file_upload='/media/resume.pdf')
		self.content =ContentManagement.objects.create(
			author_id=self.account.pk, title='abc', body='xyz', 
			summary='dhh', categories='sport', file_upload='/media/resume.pdf')
	

	def test_create_content(self):
		url = reverse('content management')
		login_url = reverse('login')
		# import pdb;pdb.set_trace()
		data = {'email':'sarveshsingh@gmail.com','password':'Sarvesh@123'}
		response = self.client.post(login_url, data, 
			content_type='application/json')
		response = json.loads(response.content)
		token = response['token']
		data = {"title":"mtv", "body":"sssss", "summary":"dddd", 
		"categories":"tv", "file_upload":open(
			'/home/dell/Downloads/resume.pdf', 'rb')}
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
		query_dict = QueryDict('', mutable=True)
		query_dict.update(data)
		response = client.post(url, data=data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		data = {"title":"mtv", "body":"sssss", "summary":"dddd", 
		"categories":"tv", "file_upload":open(
			'/home/dell/Downloads/PIP.xlsx', 'rb')}
		response = client.post(url, data=data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		data = {"title":"mtv", "summary":"dddd", 
		"categories":"tv", "file_upload":open(
			'/home/dell/Downloads/resume.pdf', 'rb')}
		response = client.post(url, data=data)
		self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

	def test_get_content(self):
		url = reverse('content management')
		login_url = reverse('login')
		data = {'email':'sarveshsingh@gmail.com','password':'Sarvesh@123'}
		response = self.client.post(login_url, data, 
			content_type='application/json')
		response = json.loads(response.content)
		token = response['token']
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
		response = client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		client.credentials(HTTP_AUTHORIZATION='Bearer ' + '')
		response = client.get(url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


	def test_update_content(self):
		url = reverse('content management')
		login_url = reverse('login')
		data = {'email':'sarveshsingh@gmail.com','password':'Sarvesh@123'}
		response = self.client.post(login_url, data, 
			content_type='application/json')
		response = json.loads(response.content)
		token = response['token']
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
		data = {"id":self.content.pk,"title":"sport"}
		user_encode_data = json.dumps(data).encode('utf-8')
		response = client.put(url, data=user_encode_data, 
			content_type='application/json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_delete_content(self):
		url = reverse('content management')
		login_url = reverse('login')
		data = {'email':'sarveshsingh@gmail.com','password':'Sarvesh@123'}
		response = self.client.post(login_url, data, 
			content_type='application/json')
		response = json.loads(response.content)
		token = response['token']
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
		data = {"id":self.content.pk}
		user_encode_data = json.dumps(data).encode('utf-8')
		response = client.delete(url, data=user_encode_data, 
			content_type='application/json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		response = client.delete(url, data=user_encode_data, 
			content_type='application/json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
	
