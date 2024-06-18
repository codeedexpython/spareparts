from rest_framework import serializers
from.models import *
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
    
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'firstname', 'lastname','email','phone_number']

# Vehicle related serializers

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'image']

class VehicleSerializer(serializers.ModelSerializer):
    brand_id = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), source='brand', write_only=True)
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Vehicle
        fields = ['id', 'name', 'image', 'brand_id', 'brand']


# Product related serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'image', 'name']

class YearSerializers(serializers.ModelSerializer):
    class Meta:
        model = ModelYear
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(many=True, read_only=True)
    vehicle_ids = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(),source='vehicle',many=True,write_only=True)
    brand = BrandSerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), source='brand', write_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    model = YearSerializers(many=True, read_only=True)
    model_ids = serializers.PrimaryKeyRelatedField(
        queryset=ModelYear.objects.all(),source='model_year',many=True,write_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'image', 'price', 'highlights', 'description', 'created_at',
            'vehicle', 'vehicle_ids', 'brand', 'brand_id', 'category', 'category_id',
            'model', 'model_ids'
        ]

class ReviewSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    product = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product_id', 'product', 'user_id', 'user', 'rating', 'comment', 'created_at']

# Cart related serializers

class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'product', 'quantity', 'cart']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'user_id', 'updated_at', 'items']