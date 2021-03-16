from rest_framework import serializers
from content_management.models import ContentManagement

class ContentManagementSerializer(serializers.ModelSerializer):
	# file = serializers.FileField(
 #        max_length=None, use_url=True,
 #    )
	content_management = serializers.SerializerMethodField()
	class Meta:
		model = ContentManagement
		fields = '__all__'

	def create(self, validated_data):
		return ContentManagement.objects.create(**validated_data)
