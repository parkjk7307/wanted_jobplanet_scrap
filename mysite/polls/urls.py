from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from .views import *


app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'), 
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/vote/', views.vote, name='vote'), 
    path('<int:question_id>/result/', views.result, name='result'), 
    path('signup/', SignupView.as_view()),
    
]