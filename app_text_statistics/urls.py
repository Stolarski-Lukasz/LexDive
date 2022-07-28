from django.urls import path
from . import views

urlpatterns = [
    path('count_tokens/', views.count_tokens, name='count_tokens'),
    path('count_types/', views.count_types, name='count_types'),
    path('count_lemmas/', views.count_lemmas, name='count_lemmas')
  
]
