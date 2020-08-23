from rest_framework import generics, permissions
from .serializers import TodoSerializer
from todo.models import Todo


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
        return Todo.objects.filter(user=user, id=self.kwargs['pk'])

