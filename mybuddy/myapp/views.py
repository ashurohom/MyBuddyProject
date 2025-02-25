from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Pet, Adoptionrequest, Donar, Contact
import re
import razorpay
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage



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

        if n=="" or e=="" or p=="" or rp=="":
            context['error_msg']="All Fields Are Required"
            return render(request,'signup.html',context)
        
        elif not re.match(r'^(?=.*[a-zA-Z])[a-zA-Z0-9._%+-]+@[a-zA-Z]+\.[a-zA-Z]{2,3}$', e):
            context['error_msg'] = "Invalid Email Format"
            return render(request, 'signup.html', context)
        
        elif p != rp:
            context['error_msg']="Password Doesnot Match"
            return render(request,'signup.html',context)
        
        elif len(n) < 3:
            context['error_msg'] = "Username must be at least 3 characters long"
            return render(request, 'signup.html', context)
        
        elif len(p) <6 or len(rp) <6:
        # elif len(p) < 6 or not re.search(r'[A-Z]', p) or not re.search(r'[a-z]', p) or not re.search(r'\d', p) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', p):    

                context['error_msg']="Password Contain Atleast 6 Character"
                #context['error_msg']="Password must be 6 chars, include uppercase, lowercase, number & symbol"
                
                return render(request,'signup.html',context)

        elif User.objects.filter(username=n).exists(): 
            context['error_msg'] = "User with this username already exists"
            return render(request, 'signup.html', context) 

        elif User.objects.filter(email=e).exists():       
            context['error_msg'] = "User with this email already exists"
            return render(request, 'signup.html', context)
        
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
                context['error_msg']="Invalid Username Or Password"
                return render(request,'signin.html',context)
    else:    
        return render(request,'signin.html')


def ulogout(request):
    logout(request)
    messages.success(request, "User logged out")
    return redirect('/signin')



def petgallery(request):
    context={}
    pet=Pet.objects.all()
    context['pets']=pet
    if not request.user.is_authenticated:
        context['message'] = "Please Login First"
    return render(request,'petgallery.html',context)



def petdetails(request,pid):
    context={}
    pets=Pet.objects.filter(id=pid)
    context['pet']=pets
    return render(request,'petdetails.html',context)



def filterbycategory(request,cid):
    context={}
    cat = Pet.objects.filter(category=cid)
    context['pets'] = cat
    return render(request,'petgallery.html',context)

    



def request_form(request, pid):
    context = {}
    pet = Pet.objects.get(id=pid)
    context['pet'] = pet

    if request.method == 'POST':
        u = User.objects.get(id=request.user.id)
        f_name = request.POST.get('full_name')
        p_number = request.POST.get('phone')
        s_address = request.POST.get('street')
        citys = request.POST.get('city')
        states = request.POST.get('state')
        z_code = request.POST.get('zip')

        #Convert string to Boolean (for dropdowns)
        experience = request.POST.get('experience')
        otherpets = request.POST.get('other_pets')

        # Ensure correct Boolean conversion
        experience = experience == "True"
        otherpets = otherpets == "True"

        # Checkbox fields (optional fields)
        regular_checkups = request.POST.get('checkups') == 'on'
        safe_home = request.POST.get('loving_home') == 'on'
        reason = request.POST.get('reason')
        acknowledgments = request.POST.get('terms') == 'on'

        # Corrected phone number validation
        if not re.fullmatch(r"[6-9]\d{9}", p_number):
            context["error_msg"] = "Warning: Incorrect Mobile Number"
            return render(request, 'request.html', context)

        # Store data in database
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

    return render(request, 'request.html', context)
 



def thanku(request):   
    context={}
    user_request = Adoptionrequest.objects.filter(userid=request.user.id).last()
    # print("Adoption_Request:", user_request)
    return render(request,'thanku.html',{'adoption_request': user_request})


def update_adoption_status(request, request_id):
    adoption_request = Adoptionrequest.objects.get(id=request_id)

    if request.method == "POST":
        new_status = request.POST.get("status")
        adoption_request.status = new_status
        adoption_request.save()

        # Send an email if the status is approved
        if new_status == "Approved":
            send_approval_email(adoption_request)

        return redirect("/admin/adoption-requests/")  # Redirect to admin panel

    return render(request, "update_status.html", {"adoption_request": adoption_request})




def send_approval_email(adoption_request):
    user_email = adoption_request.userid.email  

    subject = "Adoption Request Approved!"
    from_email = "ashitosh.rohom@gmail.com"

    message = render_to_string("adoption_email.html", {
        "user_name": adoption_request.full_name,
        "pet_name": adoption_request.pet_name,
    })

    email = EmailMessage(subject, message, from_email, [user_email])
    email.content_subtype = "html" 
    email.send()


def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method == "POST":
        n = request.POST.get("name")
        e = request.POST.get("email")
        p = request.POST.get("phone")
        m = request.POST.get("message")

        contact = Contact.objects.create(name=n, email=e, number=p, message=m)
        contact.save()
        return render(request, 'contact.html', {"success_msg": "Your message has been sent successfully!"})

    return render(request, 'contact.html')


import re
from django.shortcuts import render, redirect
from myapp.models import Donar

def donate(request):
    context = {}
    
    if request.method == "POST":
        n = request.POST.get('name')
        add = request.POST.get('address')
        mob = request.POST.get('mobile')
        amt = request.POST.get('donation-amount')

        if not n or not add or not mob or not amt:
            context["error_msg"] = "All fields are required"
            return render(request, 'donate.html', context)
        
        elif not re.fullmatch(r"^[6-9]\d{9}$", mob):
            context["error_msg"] = "Invalid Mobile Number. Must be 10 digits & start with 6-9."
            return render(request, 'donate.html', context)
        
        elif not re.fullmatch(r'^[a-zA-Z]+$', n):
            context["error_msg"] = "Name should contain only letters."
            return render(request, 'donate.html', context)

        try:
            amt = int(amt)
            if amt <= 0:
                context["error_msg"] = "Donation amount must be a positive number"
                return render(request, 'donate.html', context)
        except ValueError:
            context["error_msg"] = "Invalid donation amount"
            return render(request, 'donate.html', context)

        d = Donar.objects.create(name=n, address=add, mobile=mob, amount=amt, userid=request.user)
        d.save()

        request.session['donor_name'] = n  
        request.session['donation_amount'] = amt
        
        return redirect('/payment') 

    return render(request, 'donate.html', context)



def payment(request):
    context={}
    donation_amount = request.session.get('donation_amount', 0)  

    client = razorpay.Client(auth=("rzp_test_2zJjEbeRT0fAQQ", "4tEfDY2fzqhAENnHpl7S03L2"))
    payment = client.order.create(data={"amount": donation_amount * 100, "currency": "INR", "receipt":"1234"})

    context['donation_amount']= donation_amount
    context['payment']=payment

    return render(request, 'payment.html', context)


def email_send(request):
    user_email = request.user.email
    donor_name = request.session.get('donor_name', 'Valued Donor')
    donation_amount = request.session.get('donation_amount', 0)
      
    
    subject = "MyBuddy Donation Payment"
    from_email = "ashitosh.rohom@gmail.com"

    message = render_to_string('email.html', {
        'donor_name': donor_name,               #request.user.username
        'donation_amount': f'₹{donation_amount}'
    })

    email = EmailMessage(subject, message, from_email, [user_email])
    email.content_subtype = "html"  
    email.send()

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


# def update_user(request, sid):
#     if request.method == "GET":
#         context = {}
#         u = User.objects.filter(id=sid).first()
#         context['user'] = u  
#         return render(request, 'update_user.html', context)

#     elif request.method == "POST":
#         u = User.objects.filter(id=sid).first()
#         n = request.POST['name']
#         e = request.POST['email']
#         u.username = n
#         u.email = e
#         u.save()
#         return redirect('/user/')
    


def update_user(request, sid):
    context = {}
    u = User.objects.filter(id=sid).first()

    if request.method == "GET":
        context['user'] = u  
        return render(request, 'update_user.html', context)

    elif request.method == "POST":
        n = request.POST['name']
        e = request.POST['email']

        if n == "" or e == "":
            context['e_msg'] = "All Fields Are Required"
            context['user'] = u
            return render(request, 'update_user.html', context)

        elif len(n) < 3:
            context['e_msg'] = "Username must be at least 3 characters long"
            context['user'] = u
            return render(request, 'update_user.html', context)

        
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,3}$', e):
            context['e_msg'] = "Invalid Email Format"
            context['user'] = u
            return render(request, 'update_user.html', context)

        elif User.objects.filter(email=e).exclude(id=sid).exists():
            context['e_msg'] = "Email Already Registered"
            context['user'] = u
            return render(request, 'update_user.html', context)

        else:
            u.username = n
            u.email = e
            u.save()
            return redirect('/user/')

    return render(request, 'update_user.html', context)

  