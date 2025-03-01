"""
URL configuration for mybuddy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import update_adoption_status

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('signin/',views.signin),
    path('logout/',views.ulogout),
    path('signup/',views.signup),
    path('petgallery/',views.petgallery),
    path('details/<pid>/',views.petdetails),
    path('filterbycategory/<cid>/',views.filterbycategory),
    path('about/',views.about),
    path('contact/',views.contact),
    path('donate/',views.donate),
    path('request_form/<pid>/',views.request_form),
    path('thanku/',views.thanku),
    path('payment/',views.payment),
    path('email_send/',views.email_send),
    path('user/',views.user),
    path('delete/<uid>/',views.Delete),
    path('update/<sid>/',views.update_user),
    path('update-status/<int:request_id>/', update_adoption_status, name='update_status'),
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
