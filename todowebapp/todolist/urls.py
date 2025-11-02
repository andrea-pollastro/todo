from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_tasks, name='get_all_tasks'),
    path('add/', views.add_task, name='add_task' )
]