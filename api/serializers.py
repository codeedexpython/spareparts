from rest_framework import serializers
from .models import *
import random
import datetime
from django.contrib.auth.hashers import make_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'email', 'phone_number', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        otp = str(random.randint(100000, 999999))
        otp_created_at = datetime.datetime.now()

        user = User(
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            otp=otp,
            otp_created_at=otp_created_at
        )
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(max_length=10, required=False)
    password = serializers.CharField(max_length=100)

    def validate(self, data):
        email = data.get('email', None)
        phone_number = data.get('phone_number', None)
        password = data.get('password', None)

        if not email and not phone_number:
            raise serializers.ValidationError('An email or phone number is required to log in.')

        if not password:
            raise serializers.ValidationError('A password is required to log in.')

        return data

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def save(self):
        email = self.validated_data['email']
        otp = self.validated_data['otp']
        new_password = self.validated_data['new_password']
        user = User.objects.get(email=email)

        if user.otp != otp:
            raise serializers.ValidationError("Invalid OTP.")

        user.password = new_password
        user.save()
        return user
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'firstname', 'lastname', 'email', 'phone_number']
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'