from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_calendar, name='render_calendar'),
]