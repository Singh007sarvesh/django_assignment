from django.shortcuts import render
from content_management.models import ContentManagement
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import jwt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings
import time
import json
from . import serializers
from content_management.models import ContentManagement
from django_assign import settings
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
from django.core.files.storage import FileSystemStorage
from django.core import serializers as core_serializer
from rest_framework import status



def get_payload(request):
	token = request.META.get('HTTP_AUTHORIZATION', 'Bearer')
	token = token.split()
	payload = jwt.decode(jwt=token[1], key=settings.SECRET_KEY, 
		algorithms=['HS256'])
	return payload

# Create your views here.
@permission_classes([IsAuthenticated])
@csrf_exempt
def content_management(request):
	try:
	    if request.method == 'POST':
	   
    		payload = get_payload(request)
	    	print(request.POST)
	    	user_id = payload['user_id']
	    	data = dict()
	    	data['author'] = user_id
	    	data['title'] = request.POST.get('title')
	    	data['body'] = request.POST.get('body')
	    	data['summary'] = request.POST.get('summary')
	    	data['categories'] = request.POST.get('categories')
	    	# print(request.FILES['file_upload'])
	    	request_file = request.FILES['file_upload'] if 'file_upload' in request.FILES else None
	    	if request_file:
		    	# fs = FileSystemStorage()
		    	data['file_upload'] = request_file
		    	contentManagementSerializer = serializers.ContentManagementSerializer(data=data)
		    	# print(contentManagementSerializer)
		    	if contentManagementSerializer.is_valid(raise_exception=True):
		    		contentManagementSerializer.validated_data
		    		contentManagementSerializer.save()
		    	return JsonResponse({"message":"Successfully Created"}, 
		    		status=status.HTTP_201_CREATED)
	    elif request.method == 'GET':
	        payload = get_payload(request)
	        data = core_serializer.serialize("json", 
	        	ContentManagement.objects.filter(author_id=payload['user_id']))
	        data = json.loads(data)
	        # print(data)
	        result = []
	        for i in data: 
	        	result.append(
	        		{'id':i['pk'],'title':i['fields']['title'],
	        	'body':i['fields']['body'],'summary':i['fields']['summary'],
	        	'file_upload':i['fields']['file_upload'],
	        	'categories':i['fields']['categories']}
	        	)
	        return JsonResponse(result, safe=False, status=status.HTTP_200_OK)
	    elif request.method == 'PUT':
	    	try:
	    		data = json.loads(request.body)
	    		if len(data)<2 or len(data)>7:
	    			return JsonResponse({"message":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
	    		result = ContentManagement.objects.filter(pk=data['id']).update(**data)
	    		if result == 0:
	    			return JsonResponse({"message":"Data Not Found"}, status=status.HTTP_404_NOT_FOUND)
	    		else:
	    			return JsonResponse({"message":"Successfully Updated"}, status=status.HTTP_200_OK)
	    	except Exception as e:
	    		return JsonResponse({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
	    elif request.method == 'DELETE':
	    	try:
	    		data = json.loads(request.body)
	    		if len(data) != 1:
	    			return JsonResponse({"message":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
	    		result = ContentManagement.objects.filter(pk=data['id']).delete()
	    		if result[0] == 0:
	    			return JsonResponse({"message":"Data Not Found"}, status=status.HTTP_404_NOT_FOUND)
	    		else:
	    			return JsonResponse({"message":"Successfully Deleted"}, status=status.HTTP_200_OK)
	    	except Exception as e:
	    		return JsonResponse({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
	    else:
	    	return JsonResponse({"message":
	    		"Please request with get or post or put or delete http method"}, status=status.HTTP_400_BAD_REQUEST)
	except Exception as e:
		return JsonResponse({"error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
