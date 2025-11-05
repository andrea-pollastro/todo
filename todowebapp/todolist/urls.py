from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path("<int:pk>/update/", views.task_update, name="task_update"),
    path("delete/", views.task_delete, name="task_delete"),
    path("new/", views.task_create, name="task_create"),
]