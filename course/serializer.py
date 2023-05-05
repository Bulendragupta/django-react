from .models import *
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate

class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(max_length=255, allow_blank=False)
    class Meta:
        model=Category
        fields=('category_id','category_name')
        
        def validate_category_name(self, value):
            if Category.objects.filter(category_name=value).exists():
                raise serializers.ValidationError("Category with this name already exists.")
            return value
        
        


class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'category')

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category_serializer = CategorySerializer(data=category_data)
        category_serializer.is_valid(raise_exception=True)
        category = category_serializer.save()
        course = Course.objects.create(category=category, **validated_data)
        return course

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category', None)
        if category_data:
            category_serializer = CategorySerializer(instance.category, data=category_data)
            category_serializer.is_valid(raise_exception=True)
            category = category_serializer.save()
            instance.category = category

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance