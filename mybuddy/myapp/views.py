from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Pet, Adoptionrequest


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
    # print(pets)
    context['pet']=pets
    return render(request,'petdetails.html',context)



def filterbycategory(request,cid):
    context={}
    cat = Pet.objects.filter(category=cid)
    context['pets'] = cat
    return render(request,'petgallery.html',context)



def request_form(request):
    if request.method == 'POST':
        # Extract pet details (assumes these come from a form)
        pet_name = request.POST.get('pname')
        pet_breed = request.POST.get('breed')
        pet_age = request.POST.get('age')
        pet_gender = request.POST.get('gender')

        # Extract user details
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone')
        street_address = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')

        # Extract form-specific information
        experience_with_pets = request.POST.get('experience') == 'on'
        other_pets = request.POST.get('other_pets') == 'on'
        regular_checkups_agreement = request.POST.get('checkups') == 'on'
        safe_home_agreement = request.POST.get('loving_home') == 'on'
        adoption_reason = request.POST.get('reason')
        acknowledgment = request.POST.get('terms') == 'on'

      
        adoption_request = Adoptionrequest.objects.create(
                pet_name=pet_name,
                pet_breed=pet_breed,
                pet_age=int(pet_age),
                pet_gender=pet_gender,
                userid=userid,
                full_name=full_name,
                phone_number=phone_number,
                street_address=street_address,
                city=city,
                state=state,
                zip_code=zip_code,
                experience_with_pets=experience_with_pets,
                other_pets=other_pets,
                regular_checkups_agreement=regular_checkups_agreement,
                safe_home_agreement=safe_home_agreement,
                adoption_reason=adoption_reason,
                acknowledgment=acknowledgment,
            )
        adoption_request.save()
        return render(request, 'thanku.html')  # Redirect to a thank-you page
    else:
        return redirect('/request_form')  # Redirect to login if the user is not authenticated

    

    






def thanku(request):
    return render(request,'thanku.html')


def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def donate(request):
    return render(request,'donate.html')
