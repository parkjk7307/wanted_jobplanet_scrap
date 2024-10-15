from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("polls/", include('polls.urls')),
    path('',views.index, name='index'),
    path('some_url',views.some_url), # + 코드 추가
]