from django.contrib import admin
from .models import Pet,Donar,Contact,AdoptionHistory
from .models import Adoptionrequest
from myapp.views import update_adoption_status,send_approval_email


admin.site.register(Pet)

# class AdoptionRequestAdmin(admin.ModelAdmin):
#     list_display = ['pet_name', 'pet_breed', 'full_name', 'phone_number', 'status']
#     actions = ['approve_request', 'reject_request']

#     def approve_request(self, request, queryset):
#         queryset.update(status='Approved')
    
#     def reject_request(self, request, queryset):
#         queryset.update(status='Rejected')

# admin.site.register(Adoptionrequest, AdoptionRequestAdmin)

class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ['pet_name', 'pet_breed', 'full_name', 'phone_number', 'status']
    actions = ['approve_request', 'reject_request']

    def save_model(self, request, obj, form, change):
        """Send an email if the status is changed to 'Approved'."""
        if change:  # Ensure this is an update, not a new object creation
            old_status = Adoptionrequest.objects.get(id=obj.id).status
            if old_status != "Approved" and obj.status == "Approved":
                send_approval_email(obj)  # Call the email function

        super().save_model(request, obj, form, change)  # Save the object

    def approve_request(self, request, queryset):
        queryset.update(status='Approved')
        for obj in queryset:
            send_approval_email(obj)  # Send email for each approved request

    def reject_request(self, request, queryset):
        queryset.update(status='Rejected')

admin.site.register(Adoptionrequest, AdoptionRequestAdmin)



class DonarAdmin(admin.ModelAdmin):   
    list_display=['id','name','address','mobile','amount','userid']
admin.site.register(Donar,DonarAdmin)    


class ContactAdmin(admin.ModelAdmin):   
    list_display=['id','name','email','number','message']
admin.site.register(Contact,ContactAdmin) 