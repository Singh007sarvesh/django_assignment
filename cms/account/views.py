from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import logout
from django.contrib import auth
import jwt
from rest_framework_jwt.settings import api_settings
import time
from account.models import Account
from rest_framework import status
# Create your views here.
import time
from . import serializers
from django_assign import settings
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

@csrf_exempt
def login(request):
	try:
		if request.method == 'POST':
			request = json.loads(request.body)
			user = authenticate(email=request['email'], 
				password=request['password'])
			if user is None:
			    return JsonResponse({"message":"User with given email and password does not exists"},
			    	status=status.HTTP_400_BAD_REQUEST)
			
			try:
			    payload = JWT_PAYLOAD_HANDLER(user)
			    jwt_token = JWT_ENCODE_HANDLER(payload)
			    # update_last_login(None, user)
			except Account.DoesNotExist:
			    return JsonResponse({"message":"User with given email and password "
			    	"does not exists"}, status=status.HTTP_400_BAD_REQUEST)
			return JsonResponse({
			    'email':user.email,
			    'token': jwt_token
			}, status=status.HTTP_200_OK)
		else:
			return JsonResponse({ "detail": "Method \"GET\" not allowed."}, status=status.HTTP_400_BAD_REQUEST)
	except Exception as e:
		return JsonResponse({"error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
def registration(request):
	if request.method == 'POST':
		request = json.loads(request.body)
		try:
			account_serializer = serializers.AccountSerializer(data=request)
			if account_serializer.is_valid(raise_exception=True):
				account_serializer.validated_data
				account_serializer.save()
			return JsonResponse({"message":"Successfully Created"}, status=status.HTTP_201_CREATED)
		except Exception as e:
			return JsonResponse({"error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	else:
		return JsonResponse({ "detail": "Method \"GET\" not allowed."}, status=status.HTTP_400_BAD_REQUEST)
