from django.contrib import admin
from .models import Pet,Donar,Contact
from .models import Adoptionrequest


# Register your models here.
admin.site.register(Pet)




class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ['pet_name', 'pet_breed', 'full_name', 'phone_number', 'status']
    actions = ['approve_request', 'reject_request']

    def approve_request(self, request, queryset):
        queryset.update(status='Approved')
    
    def reject_request(self, request, queryset):
        queryset.update(status='Rejected')

admin.site.register(Adoptionrequest, AdoptionRequestAdmin)


class DonarAdmin(admin.ModelAdmin):   
    list_display=['id','name','address','mobile','amount','userid']
admin.site.register(Donar,DonarAdmin)    


class ContactAdmin(admin.ModelAdmin):   
    list_display=['id','name','email','number','message']
admin.site.register(Contact,ContactAdmin) 