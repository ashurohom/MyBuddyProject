from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    return render(request,'index.html')


def signup(request):
    if request.method == 'POST':
        n = request.POST['name']
        e = request.POST['email']
        p = request.POST['password']
        rp = request.POST['rpassword']

        print(n,e,p,rp)
    else:    
        return render(request,'signup.html')


def signin(request):
    return render(request,'signin.html')

def petgallery(request):
    return render(request,'petgallery.html')

def viewpetdetails(request):
    return render(request,'viewpetdetails.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def donate(request):
    return render(request,'donate.html')
