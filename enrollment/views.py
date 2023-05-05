from .serializer import *
from .models import *
from course.serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from django.shortcuts import get_object_or_404
    

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