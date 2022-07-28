from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index')
    # path('load_file/', views.load_file, name='help')
]
