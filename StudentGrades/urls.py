from django.urls import path

from . import views

urlpatterns = [
    path('', views.greet, name='greet'),
    path("<str:name>", views.info, name='info')
]