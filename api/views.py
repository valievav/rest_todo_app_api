from rest_framework import generics, permissions, status
from .serializers import TodoSerializer, TodoCompleteSerializer
from todo.models import Todo
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login


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
            user = User.objects.create_user(user=data['username'], password=data['password'])
            user.save()
            login(request, user)
            return JsonResponse({'token': 'we34ffv`112@#__)$)$@fxgf5'}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return JsonResponse({'error': 'That username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({'error': 'Only POST methods are supported.'}, status=status.HTTP_400_BAD_REQUEST)
