from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serilaizes import UserSerializer, GroupSerializer
from django.http import HttpResponse
from django.views.generic.base import View
from django.forms.models import model_to_dict
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from django.core import serializers



class ListUsers(View):
    """
    View to list all users in the system.
    """
    def get(self,request):
        """
        Return a list of all users.
        """
        # 返回用户名列表
        user_list = []
        users=User.objects.all()

        for user in users:
           #user_dict = model_to_dict(user)
           user_list.append(user)
           #json_list=json.dumps(user_list)
           json_list = serializers.serialize('json', user_list)
        return HttpResponse(json_list, content_type="application/json")


# 第一种方式：APIView
class UserList(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users,many=True, context={'request': request})

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# 第二种方式：通用视图 ListCreateAPIView
class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# 第三种方式：装饰器 api_view
@api_view(['GET', 'POST'])
def user_list(request):
    '''
    List all tasks, or create a new task.
    '''
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# @第四种方式：通用视图generics.ListCreateAPIView
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

    def list(self, request):
        # Note the use of get_queryset() instead of self.queryset
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

#@第五种方式： viewsets
class UserViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    允许组查看或编辑的API路径。
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

