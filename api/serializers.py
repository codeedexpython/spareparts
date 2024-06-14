from rest_framework import serializers
from.models import *

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
        queryset=ModelYear.objects.all(),source='model',many=True,write_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'image', 'price', 'highlights', 'description', 'created_at',
            'vehicle', 'vehicle_ids', 'brand', 'brand_id', 'category', 'category_id',
            'model', 'model_ids'
        ]