from django.contrib import admin
from .models import *
#from mptt.admin import MPTTModelAdmin
from .models import Project
from django_mptt_admin.admin import DjangoMpttAdmin


class ProjectAdmin(DjangoMpttAdmin):
    pass

# # Register your models here.
admin.site.register(Furniture)
admin.site.register(Vehicle_identification)
admin.site.register(Furniture_pictures)
admin.site.register(Furniture_likes)
admin.site.register(Vehicle_likes)
admin.site.register(Message)
admin.site.register(Vehicle_pictures)
admin.site.register(Profile)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Comment)


""" @admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'vehicle', 'body', 'active', 'image')
    list_filter = ('active',)
    search_fields = ('name', 'body') """

""" @admin.register(Vehicle_identification)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('owner', 'project_base', 'name', 'vehicle_description', 'slug', 'build_techniques', 'view_count')
    search_fields = ('vehicle_description', 'project_base', 'name')
    raw_id_fields = ('owner',)
  
    def get_like_count(self, obj):
        return obj.post.count()

    get_like_count.admin_order_field = "post.count()"
    get_like_count.short_description = 'View likes' """