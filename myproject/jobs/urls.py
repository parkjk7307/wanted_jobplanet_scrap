from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),  # 기본 경로를 job_list 뷰로 연결
]