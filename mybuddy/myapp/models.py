from django.db import models
from django.contrib.auth.models import User  # Default User model


# Create your models here.
class Pet(models.Model):
    CAT=((1,"Indies"),(2,"Pugs"),(3,"German"),(4,"Bulldog"),(5,"Labrador"),(6,"Combai"))
    pname = models.CharField(max_length=50)
    category = models.IntegerField(choices=CAT, verbose_name="Pet Name")
    gender = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.IntegerField()
    vaccination = models.CharField(max_length=100)
    surgery = models.CharField(max_length=100)
    description = models.CharField(max_length=300, verbose_name="Details")
    is_active = models.BooleanField(default=True, verbose_name="Is_Available")
    image = models.ImageField(upload_to='image')
    

    def __str__(self):
        return self.pname
    


    

class Adoptionrequest(models.Model):

    
    # user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user')
    # pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='adoption_requests')


    pet_name = models.CharField(max_length=100)  # Displayed, fetched from the database
    pet_breed = models.IntegerField()  # Displayed, fetched from the database
    pet_age = models.IntegerField()  # Displayed, fetched from the database
    pet_gender = models.CharField(max_length=10)  # Displayed, fetched from the database

    
    userid = models.ForeignKey("auth.User",on_delete=models.CASCADE, db_column="userid") 
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    
    experience_with_pets = models.BooleanField()  # Dropdown: Yes/No
    other_pets = models.BooleanField()  # Dropdown: Yes/No
    regular_checkups_agreement = models.BooleanField(default=False)  # Checkbox
    safe_home_agreement = models.BooleanField(default=False)  # Checkbox
    adoption_reason = models.TextField()
    acknowledgment = models.BooleanField(default=False)  # Checkbox

    # Request Metadata
    status = models.CharField(
        max_length=10,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.pet_name}"
