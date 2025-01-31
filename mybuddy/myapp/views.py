from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Pet, Adoptionrequest, Donar
import re
import razorpay
from django.core.mail import send_mail
from django.contrib import messages


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
            # print(user)
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

    if request.method == 'POST':

        # u = User.objects.filter(id=request.user.id)
        u = User.objects.get(id=request.user.id)        
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
                pet_breed=pet.category,
                pet_age=pet.age,
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
        return redirect('/thanku') 
    else:
        return render(request,'request.html',context)  




def thanku(request):
   
    context={}
    user_request = Adoptionrequest.objects.filter(userid=request.user.id).last()
    # print("Adoption_Request:", user_request)
    return render(request,'thanku.html',{'adoption_request': user_request})

# def adoption_status(request):
#     user_request = AdoptionRequest.objects.filter(user_name=request.user).last()
#     return render(request, 'adoption_status.html', {'request': user_request})








def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')



# def donate(request):
#     context = {}
#     if request.method == "POST":
#         n = request.POST.get('name')
#         add = request.POST.get('address')
#         mob = request.POST.get('mobile')
#         amt = int(request.POST.get('donation-amount'))  

#         d=Donar.objects.create(name=n,address=add,mobile=mob,amount=amt)
#         d.save()
        
#         # print(f"Name: {name}, Address: {address}, Mobile: {mobile}, Amount: {amount}")
#     return render(request, 'donate.html', context)



def donate(request):
    context = {}
    if request.method == "POST":
        n = request.POST.get('name')
        add = request.POST.get('address')
        mob = request.POST.get('mobile')
        amt = int(request.POST.get('donation-amount'))  

        if re.match("[6-9]\d{9}",mob):
            d = Donar.objects.create(name=n, address=add, mobile=mob, amount=amt, userid=request.user)
            d.save()
            request.session['donation_amount'] = amt
            return redirect('/payment') 
        else:
                context["error_msg"] = "Warning : Incorrect Mobile Number"
                return render(request,'donate.html',context)

    return render(request, 'donate.html', context)



def payment(request):
    # Retrieve the donation amount from the session
    context={}
    donation_amount = request.session.get('donation_amount', 0)  # Default to 0 if not found

    client = razorpay.Client(auth=("rzp_test_2zJjEbeRT0fAQQ", "4tEfDY2fzqhAENnHpl7S03L2"))
    payment = client.order.create(data={"amount": donation_amount * 100, "currency": "INR", "receipt":"1234"})

    context['donation_amount']= donation_amount
    context['payment']=payment

    return render(request, 'payment.html', context)



def email_send(request):
    send_mail(
        "MyBuddy Donation Payment",
        "Dear Donar Thank You, Your Donation Amount Received\n Thank You \n Visit Again MyBuddy",
        "ashitosh.rohom@gmail.com",
        ['ashitoshrohom1829@gmail.com'],
        )

    return redirect('/')


def user(request):
    context={}
    u=User.objects.filter(id=request.user.id)
    context['user']=u
    return render(request,'user.html',context)

def Delete(request,uid):
    u=User.objects.filter(id=uid)
    u.delete()
    if u.exists():
        u.delete()
        messages.success(request, "User deleted successfully.") 
    else:
         messages.error(request, "User not found.")
    return redirect('/')
    # return render(request,'user.html')


def update_user(request, sid):
    if request.method == "GET":
        context = {}
        u = User.objects.filter(id=sid).first()
        context['user'] = u  
        return render(request, 'update_user.html', context)

    elif request.method == "POST":
        u = User.objects.filter(id=sid).first()
        n = request.POST['name']
        e = request.POST['email']
        u.username = n
        u.email = e
        u.save()
        return redirect('/user/')
  