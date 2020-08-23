from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.TodoList.as_view()),
    path('todos/current/', views.TodoCurrentListCreate.as_view()),
    path('todos/completed/', views.TodoCompletedList.as_view()),
    path('todos/<int:pk>/', views.TodoRetrieveUpdateDestroy.as_view()),
]
