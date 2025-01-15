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

    


def request_form(request,pid):

    context={}
    pet = Pet.objects.get(id=pid)  
    context['pet'] = pet 

    print("Current Pet Name: ",pet.pname) 
    print("Current Pet Category: ",pet.category) 
    print("Current Pet Age: ",pet.age) 
    print("Current Pet Gender: ",pet.gender) 

    # context['data'] = {
    #         'pet_name': pet.pname,
    #         'pet_breed': pet.category, 
    #         'pet_age': pet.age,
    #         'pet_gender': pet.gender,
    #         }
            


    if request.method == 'POST':

        # u = User.objects.filter(id=request.user.id)
        u = User.objects.get(id=request.user.id)

        # uid = Adoptionrequest.objects.filter(userid = u[0])
    
        
        p_name = request.POST.get('pname')
        p_breed = request.POST.get('breed')
        p_age = request.POST.get('age')
        p_gender = request.POST.get('gender')

        
      

        f_name = request.POST.get('full_name')
        p_number = request.POST.get('phone')
        s_address = request.POST.get('street')
        citys = request.POST.get('city')
        states = request.POST.get('state')
        z_code = request.POST.get('zip')

        
        experience = request.POST.get('experience') == 'on'
        otherpets = request.POST.get('other_pets') == 'on'
        regular_checkups = request.POST.get('checkups') == 'on'
        safe_home = request.POST.get('loving_home') == 'on'
        reason = request.POST.get('reason')
        acknowledgments = request.POST.get('terms') == 'on'

      
        adoption_request = Adoptionrequest.objects.create(
                pet_name=pet.pname,
                # pet_breed=pet.p_breed,
                pet_breed=pet.category,
                # pet_age=p_age,
                pet_age=pet.age,
                # pet_gender=p_gender,
                pet_gender=pet.gender,
                userid=u,
                full_name=f_name,
                phone_number=p_number,
                street_address=s_address,
                city=citys,
                state=states,
                zip_code=z_code,
                experience_with_pets=experience,
                other_pets=otherpets,
                regular_checkups_agreement=regular_checkups,
                safe_home_agreement=safe_home,
                adoption_reason=reason,
                acknowledgment=acknowledgments,
            )
        adoption_request.save()
        return render(request,'request.html')  
    
       

    else:
        return render(request,'request.html')  

    

    






def thanku(request):
    return render(request,'thanku.html')


def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def donate(request):
    return render(request,'donate.html')
