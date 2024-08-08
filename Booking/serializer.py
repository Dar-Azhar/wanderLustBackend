from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Booking, Contact,User

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        
class RegistrationSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields =['username', 'email', 'password', 'confirmPassword']
        
    def create(self, validated_data):
        validated_data.pop('confirmPassword') 
        validated_data['password'] = make_password(validated_data['password']) 
        user = User.objects.create(**validated_data)
        return user
    def validate(self, data):
        if data['password'] != data['confirmPassword']:
            raise serializers.ValidationError("Passwords do not match.")
        
        if User.objects.filter(email = data['email'] ).exists():
            raise serializers.ValidationError("This email is already associated with another account")
        return data
