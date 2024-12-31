from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request,'index.html')

def signin(request):
    return render(request,'signin.html')

def signup(request):
    return render(request,'signup.html')

def petgallery(request):
    return render(request,'petgallery.html')

def viewpetdetails(request):
    return render(request,'viewpetdetails.html')

def about(request):
    return render(request,'about.html')
