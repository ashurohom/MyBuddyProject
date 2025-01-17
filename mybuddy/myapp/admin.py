from django.contrib import admin
from .models import Pet
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
