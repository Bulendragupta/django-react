from .serializer import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

    

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