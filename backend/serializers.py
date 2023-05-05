from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate
from . import models
from .models import *

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
		first_name = serializers.CharField(required=True)
		last_name = serializers.CharField(required=False, allow_blank=True)

		class Meta:
			model = UserModel
			fields = '__all__'
			def create(self, validated_data):
				password = validated_data.get('password') or validated_data.get('google_id', '')
				user_obj = UserModel.objects.create_user(
                email=validated_data['email'],
                username=validated_data['username'],
                password=password,
                first_name=validated_data['first_name'],
                last_name=validated_data.get('last_name', ''),
				role_id=validated_data.get('role_id', ''),
                google_id=validated_data.get('google_id', ''),
                profile_pic=validated_data.get('profile_pic', ''),
                )
				user_obj.save()
				return user_obj
			

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	##
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['email'], password=clean_data['password'])
		if not user:
			raise ValidationError('User not Found')
		return user

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		# fields = '__all__'
		fields = ('user_id','email','role_id', 'username','first_name','last_name','profile_pic')

class UserProfileSerializer(serializers.Serializer):
  username = serializers.CharField(required=True, allow_blank=False)
  email = serializers.EmailField(required=True, allow_blank=False)
  first_name = serializers.CharField(required=True, allow_blank=False)
  last_name = serializers.CharField(required=False, allow_blank=True)
  profile_pic = serializers.URLField(required=False, allow_blank=True)
  access_token = serializers.CharField(required=False, allow_blank=True)
  google_id = serializers.CharField(required=False, allow_blank=True)


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

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'