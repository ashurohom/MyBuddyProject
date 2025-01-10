from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Pet


# Create your views here.

def index(request):
    return render(request,'index.html')


def signup(request):
    context={}
    if request.method == 'POST':
        n = request.POST['name']
        e = request.POST['email']
        p = request.POST['password']
        rp = request.POST['rpassword']

        # print(n,e,p,rp)
        # return HttpResponse("Data Fetched")

        if n=="" or e=="" or p=="" or rp=="":
            context['error_msg']="All Fields Are Required"
            return render(request,'signup.html',context)
        
        elif p != rp:
            context['error_msg']="Password Doesnot Match"
            return render(request,'signup.html',context)
        
        elif len(p) <6 or len(rp) <6:
                context['error_msg']="Password Contain Atleast 6 Character"
                return render(request,'signup.html',context)
        
        else:
            u = User.objects.create(username=n, email=e)
            u.set_password(rp)
            u.save()
            return redirect('/signin')

    else:    
        return render(request,'signup.html')


def signin(request):
    context={}
    if request.method == "POST":
        un = request.POST['uname']
        up = request.POST['upass']
    
        if un == "" or up == "":
            context['error_msg']="All Fields Are Required"
            return render(request,'signin.html',context)

        else:
            user = authenticate(username=un, password=up)
            print(user)
            if user != None:
                login(request,user)
                return redirect('/') 
            else:
                context['error_msg']="Invalid Username And Password"
                return render(request,'signin.html',context)
            

    else:    
        return render(request,'signin.html')




def ulogout(request):
    logout(request)
    return redirect('/signin')




def petgallery(request):
    context={}
    pet=Pet.objects.all()
    # print(pet)
    context['pets']=pet
    return render(request,'petgallery.html',context)



def petdetails(request,pid):
    context={}
    pets=Pet.objects.filter(id=pid)
    print(pets)
    context['pet']=pets
    return render(request,'petdetails.html',context)



def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def donate(request):
    return render(request,'donate.html')
