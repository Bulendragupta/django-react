from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate

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
			raise ValidationError('user not found')
		return user

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		# fields = '__all__'
		fields = ('user_id','email', 'username','first_name','last_name','profile_pic')

class UserProfileSerializer(serializers.Serializer):
  username = serializers.CharField(required=True, allow_blank=False)
  email = serializers.EmailField(required=True, allow_blank=False)
  first_name = serializers.CharField(required=True, allow_blank=False)
  last_name = serializers.CharField(required=False, allow_blank=True)
  profile_pic = serializers.URLField(required=False, allow_blank=True)
  access_token = serializers.CharField(required=False, allow_blank=True)
  google_id = serializers.CharField(required=False, allow_blank=True)