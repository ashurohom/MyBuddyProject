from django.db import models

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