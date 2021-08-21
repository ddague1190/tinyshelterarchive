"""final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
import website.views
from website.models import *


from django_otp.admin import OTPAdminSite
from django.contrib.auth.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin
from django_mptt_admin.admin import DjangoMpttAdmin


class ProjectAdmin(DjangoMpttAdmin):
    pass

class OTPAdmin(OTPAdminSite):
    pass


admin_site = OTPAdmin(name='OTPAdmin')
admin_site.register(User)
admin_site.register(TOTPDevice, TOTPDeviceAdmin)
admin_site.register(Furniture)
admin_site.register(Vehicle_identification)
admin_site.register(Furniture_pictures)
admin_site.register(Furniture_likes)
admin_site.register(Vehicle_likes)
admin_site.register(Message)
admin_site.register(Vehicle_pictures)
admin_site.register(Profile)
admin_site.register(Project, ProjectAdmin)
admin_site.register(Comment)











urlpatterns = [
    path('901252112/', admin.site.urls),
    path('', include('website.urls')),
    #path('tinymce/', include('tinymce.urls')),
    #url(r'^messages/', include('postman.urls', namespace='postman')),
    url('^', include('django.contrib.auth.urls'))

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
