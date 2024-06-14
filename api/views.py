from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from .serializers import *
from .models import *
from django.shortcuts import get_object_or_404


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Send OTP email
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {user.otp}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return Response({"message": "User registered successfully. OTP sent to email."},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            phone_number = serializer.validated_data.get('phone_number')
            password = serializer.validated_data.get('password')

            try:
                if email:
                    user = User.objects.get(email=email)
                elif phone_number:
                    user = User.objects.get(phone_number=phone_number)

                if not check_password(password, user.password):
                    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=request.data['email'])
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.otp_created_at = datetime.datetime.now()
            user.save()

            # Send OTP email
            send_mail(
                'Your OTP Code for Password Change',
                f'Your OTP code is {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return Response({"message": "OTP sent to email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def list_users(request):
    users = User.objects.all()
    serializer = UserDetailSerializer(users, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def user_detail_get(request, user_id):
    user = User.objects.get(user_id=user_id)
    if request.method == 'GET':
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

@api_view([ 'PUT'])
def user_detail_update(request, user_id):
    user = User.objects.get(user_id=user_id)
    if request.method == 'PUT':
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def user_detail_delete(request, user_id):
    user = User.objects.get(user_id=user_id)
    if request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['GET'])
def list_addresses(request):
    addresses = Address.objects.all()
    serializer = AddressSerializer(addresses, many=True)
    return Response(serializer.data)
@api_view(['POST'])
def create_address(request):
    if request.method == 'POST':
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_address(request, address_id):
    address = Address.objects.get(pk=address_id)
    serializer = AddressSerializer(address)
    return Response(serializer.data)


@api_view(['PUT'])
def update_address(request, address_id):
    try:
        address = Address.objects.get(pk=address_id)
    except Address.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_address(request, address_id):
    address = Address.objects.get(pk=address_id)
    if request.method == 'DELETE':
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


