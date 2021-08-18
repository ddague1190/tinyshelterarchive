from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

app_name = 'website'

urlpatterns = [
    path('genres/', views.show_genres),
    path('profile/<user>', views.ProfileMessageView.as_view(), name='profile'),
    path('editprofile/<user>', views.ProfileEditView.as_view(), name='editprofile'),
    path('vehicledeleterequest/<slug>', views.VehicleDeleteView.as_view(), name='deletevehicle'),
    path('furnituredeleterequest/<pk>', views.FurnitureDeleteView.as_view(), name='deletefurniture'),
    path('furniture/<slug>', views.ListFurnitureView.as_view(), name='list_furniture'),
    path('furnish/<slug>', views.FurnitureCreate.as_view(), name="furnish"),
    path('', views.index, name='index'),
    path('addvehicle/', views.VehicleCreate.as_view(), name='addvehicle'),
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('garage/<user>', views.GarageView.as_view(), name='garage'),
    path('editfurniture/<pk>', views.FurnitureEdit.as_view(), name='editfurniture'),
    path('editvehicle/<slug>', views.VehicleEdit.as_view(), name='editvehicle'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('furniturebytechnique/<technique>', views.FurniturebyTechnique.as_view(), name='listfurniturebytechnique'),
    path('furniturebybuilder/<builder>', views.FurniturebyBuilder.as_view(), name='furniturebybuilder'),
    path('vehicle/<slug>', views.VehicleView.as_view(), name='vehicle'),
    path('like', views.like, name='like'),
    path('deletemessage', views.deletemessage, name='deletemessage'),
    #path('projectpreview', views.projectpreview, name="projectpreview"),
    path('furniturebytype/<type>', views.FurniturebyType.as_view(), name='furniturebytype'),
    path('searchvehicles', views.VehicleSearch.as_view(), name='searchvehicles'),
    path('vehlike', views.vehlike, name='vehlike'),
    path('comment/reply/', views.reply_page, name="reply")
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

