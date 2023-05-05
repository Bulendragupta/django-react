from .validations import *
from .serializer import *
from .models import *
from django.utils import timezone
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import  login, logout
from rest_framework import permissions, status
from django.core.exceptions import ValidationError
from rest_framework.authentication import SessionAuthentication

def index(request):
    return render(request, 'index.html')


class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            clean_data = custom_validation(request.data)
        except ValidationError as e:
            errors = e.message_dict
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid():
            user = serializer.create(clean_data)
            user.created_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
            user.save() # Save the user object to persist the created_ip attribute
            success = 'Created Successfully'
            data = {'Result':success,'username': user.username, 'email': user.email}
            return Response( data, status=status.HTTP_201_CREATED)

        errors = serializer.errors
        return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_password(data)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            session_id = request.session.session_key
            user.last_ip = request.META.get('REMOTE_ADDR')
            user.session_id = session_id
            user.is_loggedin = True
            user.save()
            data = {'User LoggedIn Successfully':True, 'username': user.username, 'email': user.email}
            return Response(data, status=status.HTTP_200_OK)
        

class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'User Details': serializer.data}, status=status.HTTP_200_OK)


class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response({'User Logout Successfully:True'}, status=status.HTTP_200_OK)



class user_profile(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            profile_pic = serializer.validated_data['profile_pic']
            access_token = serializer.validated_data['access_token']
            google_id = serializer.validated_data['google_id']
            if google_id is None or google_id.strip() == '':
                google_id = 'manual'
            user_profile = None
            try:
                user_profile = AppUser.objects.get(username=username)
            except AppUser.DoesNotExist:
                pass
            if user_profile:
                if user_profile.email == email:
                    user_profile.last_ip = request.META.get('REMOTE_ADDR')
                    user_profile.last_login = timezone.now()
                    user_profile.access_token = serializer.validated_data['access_token']
                    user_profile.save()
                    return Response({'Profile_Updated': True})
                else:
                    return Response({'email': ['User profile with this email already exists.']}, status=400)
            else:
                try:
                    user_profile = AppUser.objects.get(email=email)
                except AppUser.DoesNotExist:
                    pass
                if user_profile:
                    return Response({'username': ['User profile with this username already exists.']}, status=400)
                else:
                    user_profile = AppUser.objects.create(username=username, email=email, first_name=first_name, last_name=last_name, profile_pic=profile_pic,access_token=access_token,google_id=google_id)
                    user_profile.created_ip = request.META.get('REMOTE_ADDR')
                    user_profile.save()
                    return Response({'Successfully_Created': True})
        return Response(serializer.errors, status=400)