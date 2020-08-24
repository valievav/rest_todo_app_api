from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser

from todo.models import Todo
from .serializers import TodoSerializer, TodoCompleteSerializer


# to view list of ALL todos
class TodoList(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('-created')


# to view active todos, add new todos
class TodoCurrentListCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user  # show results only for logged in user
        queryset = Todo.objects.filter(user=user, datecompleted__isnull=True).order_by('-created')
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # set user to the current user automatically


# to view completed todos
class TodoCompletedList(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user  # show results only for logged in user
        queryset = Todo.objects.filter(user=user, datecompleted__isnull=False).order_by('-datecompleted')
        return queryset


# to view certain todos, update, delete
class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)


# to update certain todos
class TodoCompleteUpdate(generics.UpdateAPIView):
    serializer_class = TodoCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.instance.datecompleted = timezone.now()  # set auto
        serializer.save()


# to create new user and login (only POST allowed)
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(data['username'], password=data['password'])
            user.save()
            token = Token.objects.create(user=user)  # generating user token
            return JsonResponse({'token': str(token)}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return JsonResponse({'error': 'That username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({'error': 'Only POST methods are supported.'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(request, username=data['username'], password=data['password'])
        if not user:
            return JsonResponse({'error': 'Could not login. Please check username and password.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)  # generating user token

        return JsonResponse({'token': str(token)}, status=status.HTTP_200_OK)

    return JsonResponse({'error': 'Only POST methods are supported.'}, status=status.HTTP_400_BAD_REQUEST)
