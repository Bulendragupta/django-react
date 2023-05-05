from .validations import *
from .serializers import *
from .models import *
from .models import AppUser
from django.utils import timezone
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import  login, logout
from rest_framework.decorators import api_view
from rest_framework import permissions, status
from rest_framework import generics
from django.core.exceptions import ValidationError
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

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


class CategoryCreateView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    
    def post(self, request, format=None):
        category_name = request.data.get('category_name')
        if Category.objects.filter(category_name=category_name).exists():
            return Response({'Category already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Category Successfully Created': True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, category_id=None):
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                return Response({"error": "Category does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def put(self, request, category_id=None):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, category_id=None):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category does not exist"}, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # def get(self, request, user_id):
    #     courses = Course.objects.filter(user=user_id)
    #     serializer = CourseSerializer(courses, many=True)
    #     return Response(serializer.data)
    
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response({'courses': serializer.data}, status=status.HTTP_200_OK)


    def post(self, request, user_id):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            category_data = serializer.validated_data.pop('category')
            category_view = CategoryCreateView()
            category = category_view.create(request, category_data).data
            course = serializer.save(user_id=user_id, category_id=category['id'])
            return Response(CourseSerializer(course).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id, course_id):
        try:
            course = Course.objects.get(id=course_id, user=user_id)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            category_data = serializer.validated_data.pop('category')
            category_view = CategoryCreateView()
            category = category_view.update(request, course.category.id, category_data).data
            course = serializer.save(user_id=user_id, category_id=category['id'])
            return Response(CourseSerializer(course).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, course_id):
        try:
            course = Course.objects.get(id=course_id, user=user_id)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        category_id = course.category.id
        course.delete()
        category_view = CategoryCreateView()
        category_view.delete(request, category_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class EnrollmentView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id):
        user = request.user
        course = Course.objects.get(id=course_id)
        data = request.data
        data['user'] = user.id
        serializer = EnrollmentSerializer(data=data)
        if serializer.is_valid():
            enrollment = serializer.save(course=course)
            return Response({'enrollment_id': enrollment.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CourseView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        serializer = CourseSerializer(course)
        enrolled_users = course.enrollment_set.filter(user=request.user)
        role = None
        if enrolled_users.exists():
            role = enrolled_users.first().role

        if role is None or role == Role.GET:
            serializer = CourseSerializer(course, exclude=('content',))

        if role == Role.GET or role == Role.UPDATE:
            return Response(serializer.data)

        if role == Role.ADMIN:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
