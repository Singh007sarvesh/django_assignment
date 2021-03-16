from rest_framework import serializers
from account.models import Account
import re
from django.contrib.auth.hashers import make_password

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'


    def update(self, instance, validated_data):

        instance.description = validated_data["password"]
        instance.name = validated_data["name"]

        instance.save()

        return instance

    def validate(self, data):
    	password = data['password']
    	if type(data['pincode']) != int:
    		raise serializers.ValidationError("Please enter valid pin number")
    	pincode = str(data['pincode'])
    	regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$";
    	temp = re.compile(regex); 
    	pin_number = re.match(temp, pincode);
    	if len(password)<8:
    		raise serializers.ValidationError("password length should be at least 8")
    	if not any(char.isupper() for char in password):
    		raise serializers.ValidationError("Password should have at least one uppercase letter")
    	if not any(char.islower() for char in password):
    		raise serializers.ValidationError("Password should have at least one lowercase letter")
    	if pin_number is None or pincode == '':
    		raise serializers.ValidationError("Please enter valid pin number")
    	return data    

    def create(self, validated_data):
    	validated_data['password'] = make_password(validated_data['password'])
    	return super(AccountSerializer, self).create(validated_data)