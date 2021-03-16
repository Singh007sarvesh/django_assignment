from django.test import TestCase
from account.models import Account
from django.urls import reverse
from rest_framework import status
import json
from django.contrib.auth.hashers import make_password
# Create your tests here.


class AccountTestCase(TestCase):
    def setUp(self):
    	password = make_password('Anurag@21')
    	self.account = Account.objects.create(email="sarvesh3@gmail.com", 
        	first_name="Sarvesh", last_name='Singh', address='Roopena',
        	city='Bangalore', state='Karnataka', country='India',
        	phone='+918896052348',password=password,pincode=564433)
    def test_create_account(self):
    	url = reverse('registrations')
    	data = {"email":"amitsingh@gmail.com", "first_name":"xyz", "last_name":"abc", "phone":"+919480695563", "pincode":"122454", "password":"Sarvesh21"}
    	user_encode_data = json.dumps(data, indent=4).encode('utf-8')
    	response = self.client.post(url, user_encode_data, content_type='application/json')
    	self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    	response = self.client.post(url, user_encode_data, content_type='application/json')
    	self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    	self.assertEqual(url, '/api/v1/registrations/')
    	self.assertEqual(self.account.email,'sarvesh3@gmail.com')
    	self.assertEqual(self.account.pk,1)

    def test_login(self):
    	url = reverse('login')
    	data = {'email':'sarvesh3@gmail.com','password':'Anurag@21'}
    	response = self.client.post(url, data, 
    		content_type='application/json')
    	self.assertEqual(response.status_code, status.HTTP_200_OK)
    	data = {'email':'sarvesh3@gmail.com','password':'Anurag'}
    	response = self.client.post(url, data, 
    		content_type='application/json')
    	self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)