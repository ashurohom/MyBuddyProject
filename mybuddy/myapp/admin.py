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

    def approve_request(self, request, queryset):
        for obj in queryset:
            if obj.status != "Approved":
                obj.status = "Approved"
                obj.save()

                # Send approval email
                send_approval_email(obj)

                # Save pet details in history table
                AdoptionHistory.objects.create(
                    user=obj.id,  # Assuming 'userid' is a ForeignKey to User
                    pet_name=obj.pname,
                    pet_breed=obj.category
                )

                # Delete the pet from the database
                Pet.objects.filter(id=obj.pet_id).delete()

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