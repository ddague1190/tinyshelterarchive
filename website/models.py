from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.utils.translation import gettext, gettext_lazy
from multiselectfield import MultiSelectField
from django.urls import reverse
from django.utils.text import slugify
from django_resized import ResizedImageField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_bleach.models import BleachField
from mptt.models import MPTTModel, TreeForeignKey


User._meta.get_field('email')._unique = True

class Project(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    tree_linked = models.BooleanField(default=True)
    can_be_parent = models.BooleanField(default=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    like_count = models.PositiveIntegerField(default=0)
    
    class MPTTMeta:
        order_insertion_by = ['like_count']

    def __str__(self):
        return self.name


Technique_choices = [
        ('aluminum extrusions', 'aluminum extrusions'),
        ('welding', 'welding'),
        ('carpentry', 'carpentry'),
        ('fiberglass', 'fiberglass'),
        ('CNC', 'CNC'),
        ('foam', 'foam')
        ]

Function_choices = [
        ('Kitchen', 'Kitchen'),
        ('Bathroom', 'Bathroom'),
        ('Bedroom', 'Bedroom'),
        ('Garage', 'Garage'),
        ('Workspace', 'Workspace'),
        ('Utilities', 'Utilities')
    ]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = BleachField()
    location = models.CharField(max_length=30, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='uploads/profile_pic', default='static/profile_pic_default.png', null=True, blank=True)
    website = models.URLField(max_length=100, default=None, null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)

#reference https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Profile.objects.create(user=instance)

#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.profile.save()

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()   

class Vehicle_identification(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    project_base = models.CharField('Project Base', max_length=100)
    name = models.CharField('Name', max_length=150, unique=True)
    vehicle_description = models.TextField()
    
    vehicle_description = BleachField(allowed_tags=[
       'p', 'b', 'i', 'u', 'em', 'strong', 'a',
        'img', 'h3', 'h4', 'h5', 'h6'])
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    build_techniques = models.CharField('Predominant build technique', choices=Technique_choices, max_length=20)
    view_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Vehicle_identification, self).save(*args, **kwargs)

    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)

class Comment(models.Model):
    vehicle = models.ForeignKey(Vehicle_identification, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField()
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='uploads/comment_pictures', null=True, blank=True)


    def __str__(self):
        return self.body
    
    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)

class Vehicle_pictures(models.Model):
    image = models.ImageField(upload_to ='uploads/vehicle_pictures', null=True)
    parent = models.ForeignKey(Vehicle_identification, on_delete=models.CASCADE, related_name='images')
    annotation = models.TextField(blank=True)

    # def __str__(self):
    #     return self.pk

class Vehicle_likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Vehicle_identification, on_delete=models.CASCADE, related_name='post')

class Furniture(models.Model):
    room = models.CharField('Category', unique=True, max_length=100)
    builder = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    vehicle = models.ForeignKey(Vehicle_identification, on_delete=models.CASCADE, related_name='furnitures')
    functionality = models.CharField('Predominant functionality', choices=Function_choices, max_length=20)
    description = BleachField()

class Furniture_pictures(models.Model):
    image = models.ImageField(upload_to ='uploads/furniture_pictures', null=True)
    parent = models.ForeignKey(Furniture, on_delete=models.CASCADE, related_name='images')
    annotation = models.TextField(blank=True)

class Furniture_likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Furniture, on_delete=models.CASCADE, related_name='post')

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipient")
    read = models.BooleanField(default=False)
    subject = models.CharField(max_length=80)
    message = BleachField()
    sent_at = models.DateTimeField(auto_now_add=True)
    


