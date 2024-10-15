from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world.")


def some_url(requset): # + 코드추가
    return HttpResponse("some url를 구현해 봤습니다.")