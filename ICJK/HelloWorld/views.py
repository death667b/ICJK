from django.shortcuts import render
from django.http import HttpResponse
from .models import TextItem


def index(request):
    return render(request, 'HelloWorld/index.html',{'elements':TextItem.objects.all()})