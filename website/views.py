# Credits: "Ordinarycoders.com" for tutorial on using Django's userauthenticationsystem (see register, login_request, logout functions)

from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.forms.models import modelform_factory
from multiselectfield.db.fields import add_metaclass
from website.models import Furniture_pictures, Vehicle_identification, Furniture, Vehicle_pictures
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from .forms import *
from .models import *
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.forms.models import inlineformset_factory
from django.db import transaction
from django import forms
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from website.tokens import account_activation_token
from django.utils.encoding import force_text, force_bytes
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
import json
from django.views import View
from django.views.generic.detail import DetailView, BaseDetailView
from django.utils.text import slugify
from .utils import url_tag, image_path, number_extractor
from django.db.models import Q





def show_genres(request):
    return render(request, "website/projects.html", {'projects': Project.objects.all()})


def index(request):
    return render(request, "base.html", {'projects': Project.objects.all()})

# credit https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
def register(request):
    if request.method == "POST":
        user_form = NewUserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active=False
            user.save()
            user.refresh_from_db()
            profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
            profile_form.full_clean()
            image =  profile_form.cleaned_data['profile_pic']
            profile_form.save()
            current_site = get_current_site(request)
            subject = 'Please activate your Tiny Shelter Archives Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            messages.info(request, "We sent an email to your email account. Please confirm account to finish registration.")
            return redirect('website:index')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        user_form = NewUserForm()
        profile_form = ProfileForm()
    return render(request, "register.html", {
        "user_form":user_form,
        "profile_form": profile_form,
        'projects': Project.objects.all()
        })

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        messages.info(request, "Thanks for joining the site!")

        return redirect('website:index')
    else:
        messages.error(request, "Unsuccessful registration. Invalid activation.")
        return redirect('website:index')

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Currently logged in as {username}')
                return redirect('website:index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'login.html', {"form": form, 'projects': Project.objects.all()})

def logout_request(request):
    logout(request)
    messages.info(request, "Currently logged out")
    return redirect("website:index")


class ProfileView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name= 'profile.html'
    model = User
    context_object_name = 'contributor'

    def get_object(self, **kwargs):
        user_object = User.objects.get(username=self.kwargs.get('user'))
        return user_object

    def get_sent_emails(self):
        if self.request.user != self.get_object():
            return None
        return Message.objects.filter(sender=self.request.user)   
    
    def get_recieved_emails(self):
        if self.request.user != self.get_object():
            return None
        return Message.objects.filter(recipient=self.request.user)
          
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sent_emails'] = self.get_sent_emails()
        context['recieved_emails'] = self.get_recieved_emails()
        context['form']=MessageForm()
        context['projects']=Project.objects.all()
        return context

class MessageView(SingleObjectMixin, FormView):
    def get_object(self, **kwargs):
        user_object = User.objects.get(username=self.kwargs.get('user'))
        return user_object

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object = self.get_object()
        form = MessageForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        message = form.save(commit=False)
        message.sender = self.request.user
        message.recipient = User.objects.get(username=self.kwargs.get('user'))
        message.save()
        messages.info(self.request, "Email sent.")
        return HttpResponseRedirect(reverse_lazy('website:profile', kwargs={'user': self.kwargs.get('user')}))



class ProfileMessageView(View):
    def get(self, request, *args, **kwargs):
        view = ProfileView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = MessageView.as_view()
        return view(request, *args, **kwargs)

class ProfileEditView(LoginRequiredMixin, UpdateView):
    login_url = 'website/login'
    redirect_field_name = 'redirect_to'
    model = Profile
    template_name = 'editprofile.html'
    form_class= ProfileForm
    success_url = None
    def get_object(self):
        user = self.kwargs.get('user')
        if user == self.request.user.username:
            return Profile.objects.get(user=self.request.user)
        else:
            raise PermissionDenied


    def get_context_data(self, **kwargs):
        context = super(ProfileEditView, self).get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        return context

    def get_success_url(self):
        return reverse('website:profile', kwargs={'user': self.request.user.username}, )

class GarageView(ListView):
    template_name = 'website/garage.html'

    model = Vehicle_pictures
    
    #def get_queryset(self):
     #   return Vehicle_pictures.objects.filter(parent__owner=self.request.user)

    def number_of_likes(self):
        garage_owner = self.kwargs.get('user')
        owner = User.objects.get(username=garage_owner)
        list = Vehicle_identification.objects.filter(owner=owner)
        number_of_likes_dictionary = {}
        for item in list:
            number_of_likes_dictionary[item.pk]=item.post.count()
        return number_of_likes_dictionary

    def get_context_data(self, **kwargs):
        garage_owner = self.kwargs.get('user')
        owner = User.objects.get(username=garage_owner)
        image_list = Vehicle_pictures.objects.filter(parent__owner=owner)
        context = super(GarageView, self).get_context_data(**kwargs)
        context['vehicle_list'] = Vehicle_identification.objects.filter(owner=owner)
        #context['image_list']=image_list
        context['garage_owner']=garage_owner
        context['furniture_image_list'] = Furniture_pictures.objects.filter(parent__builder=owner)
        context['projects'] = Project.objects.all() 
        context['like_ref'] = self.number_of_likes()   
        return context

class ListFurnitureView(ListView):
    template_name = 'website/list_furniture.html'
    context_object_name = 'furniture_list'
    this_vehicle = None

    def get_queryset(self):
        slug=self.kwargs.get('slug')
        vehicle_object = Vehicle_identification.objects.get(slug=slug)
        self.this_vehicle = vehicle_object
        return Furniture.objects.filter(vehicle=vehicle_object).order_by('functionality')

    def number_of_likes(self):
        furniture_list = self.get_queryset()
        number_of_likes_dictionary = {}
        for item in furniture_list:
            number_of_likes_dictionary[item.pk]=item.post.count()
        return number_of_likes_dictionary

    def get_context_data(self, **kwargs):
        image_list = Furniture_pictures.objects.filter(parent__vehicle=self.this_vehicle)
        context = super(ListFurnitureView, self).get_context_data(**kwargs)
        context['vehicle_name']=self.this_vehicle
        context['image_list']=image_list
        like_ref=self.number_of_likes()
        context['like_ref']=like_ref
        context['projects'] = Project.objects.all()
        return context
#https://dev.to/zxenia/django-inline-formsets-with-class-based-views-and-crispy-forms-14o6

class FurnitureCreate(LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    model = Furniture
    template_name = 'website/furniture_create.html'
    form_class = FurnitureForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(FurnitureCreate, self).get_context_data(**kwargs)
        data['projects'] = Project.objects.all()
        if self.request.POST:
            data['image_form'] = FurnitureFormset(self.request.POST)
        else:
            data['image_form'] = FurnitureFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        slug=self.kwargs.get('slug')
        vehicle = Vehicle_identification.objects.get(slug=slug)
         #Limit to 10 categories
        existing_categories = Furniture.objects.filter(vehicle=vehicle.pk).count()
        if existing_categories >= 10:
            messages.error(self.request, "Unsuccessful upload, you can only submit 10 objects\
                 - if you need more contact site owner.")
            return redirect('website:index')
        if vehicle.owner != self.request.user:
            raise PermissionDenied
        image_form = context['image_form']
        with transaction.atomic():
            form.instance.builder = self.request.user
            form.instance.vehicle = vehicle
            formset = FurnitureFormset(self.request.POST, self.request.FILES)
            self.object = form.save()
            if formset.is_valid():
                for item in formset.cleaned_data:
                    if item:
                        image = item['image']
                        annotation = item['annotation']
                        photo = Furniture_pictures(parent=form.instance, image=image, annotation=annotation)
                        photo.save()

            if image_form.is_valid():
                image_form.instance = self.object
                image_form.save()
            return super(FurnitureCreate, self).form_valid(form)

    def get_success_url(self):
        slug=self.kwargs.get('slug')
        return reverse('website:list_furniture', kwargs={'slug':slug})

class VehicleCreate(LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    model = Vehicle_identification
    template_name = 'website/vehicle_create.html'
    form_class = Vehicle_identificationForm

    def get_context_data(self, **kwargs):
        data = super(VehicleCreate, self).get_context_data(**kwargs)
        data['projects'] = Project.objects.all()
        if self.request.POST:
            data['image_form'] = Vehicle_picturesFormset(self.request.POST)
        else:
            data['image_form'] = Vehicle_picturesFormset()
        return data
    

    def form_valid(self, form):
        context = self.get_context_data()
        image_form = context['image_form']
        with transaction.atomic():
            form.instance.owner = self.request.user
            formset = Vehicle_picturesFormset(self.request.POST, self.request.FILES)
            self.object = form.save()
            file = open('django-image-formsetcreateview.txt', 'w')
            file.write(str(formset))

            if formset.is_valid():
                for item in formset.cleaned_data:
                    file.write(str(formset.cleaned_data))
                    file.close()
                    if item:
                        image = item['image']
                        annotation = item['annotation']
                        photo = Vehicle_pictures(parent=form.instance, image=image, annotation=annotation)
                        photo.save()

            if image_form.is_valid():
                image_form.instance = self.object
                image_form.save()
            

            if form.is_valid():
                project_base = form.cleaned_data.get('project_base')

                #project_base = self.request.POST['project_base']
                project_parent = Project.objects.get(name=project_base)
                project_name = form.cleaned_data.get('name')
                Project.objects.create(name=project_name, parent=project_parent)
                
            return super(VehicleCreate, self).form_valid(form) 

    def get_success_url(self):
        return reverse('website:garage', kwargs={'user':self.request.user.username})

class VehicleEdit(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    model = Vehicle_identification
    template_name = 'website/vehicle_create.html'
    form_class = Vehicle_identificationForm
    success_url = None
    old_project = None

    def get_context_data(self, **kwargs):
        slug=self.kwargs.get('slug')
        vehicle = Vehicle_identification.objects.get(slug=slug)
        self.old_project = vehicle.name
        if vehicle.owner != self.request.user:
            raise PermissionDenied
        data = super(VehicleEdit, self).get_context_data(**kwargs)
        data['projects'] = Project.objects.all()
        if self.request.POST:
            data['image_form'] = Vehicle_picturesFormset(self.request.POST)
        else:
            data['image_form'] = Vehicle_picturesFormset(instance=vehicle)
        return data
    

    def form_valid(self, form):
        context = self.get_context_data()
        image_form = context['image_form']
        with transaction.atomic():
            form.instance.owner = self.request.user
            self.object = form.save()
            form.instance = self.object
            formset = Vehicle_picturesFormset(self.request.POST, self.request.FILES, instance = self.object)
            # file = open('django-image-formset1.txt', 'w')
            # file.write(str(formset)+'\n\n\n\n\n\n\n\n')
            # print(formset.errors)
            if formset.is_valid():
        
                for item in formset.cleaned_data:
                    # file.write(str(item))
                    if item:
                        # file.write('\nBIGIF\ifitem\n')

                        if item['id']:
                            # file.write('\nif itemid&&&\n')

                            # file.write(str(item['id']))
                            if item['DELETE']:
                                # file.write('\n\tif itemid AND itemDelete929292929\n')
                                Vehicle_pictures.objects.get(pk=number_extractor(item['id'])).delete()
                            else:
                                # file.write('\n\t\tif itemID --> elseupdateannotation\n')
                                Vehicle_pictures.objects.filter(pk=number_extractor(item['id'])).update(annotation=item['annotation'])
                        else: 
                            # file.write('\nelse not ITEMID elsecreate\n')
                            image = item['image']
                            annotation = item['annotation']
                            photo = Vehicle_pictures(parent=form.instance, image=image, annotation=annotation)
                            photo.save()
                    # else:
                    #     file.write('\nBIGELSE\tnotitem\n')
                    # file.write("\n____________________________________________________________________________________\n")

            # file.write('endoftestoutput')
            # file.close()              
    
            if image_form.is_valid():
                image_form.instance = self.object
                image_form.save()

            if form.is_valid():

                #change old MPTT link out
                old_mptt_link = Project.objects.get(name=self.old_project)
                old_mptt_link.delete()
                project_base = form.cleaned_data.get('project_base')
                project_parent = Project.objects.get(name=project_base)
                project_name = form.cleaned_data.get('name')
                Project.objects.create(name=project_name, parent=project_parent)

                #update slug
                #vehicle = Vehicle_identification.objects.get(name=self.old_project)
                #vehicle.slug=slugify(project_name)
                #vehicle.save()

                return super(VehicleEdit, self).form_valid(form)
            
            else:
                return PermissionDenied


    def get_success_url(self):
        return reverse('website:garage', kwargs={'user':self.request.user.username})

class FurnitureEdit(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    model = Furniture
    template_name = 'website/furniture_create.html'
    form_class = FurnitureForm
    success_url = None

    def get_context_data(self, **kwargs):
        #slug=self.kwargs.get('slug')
        #vehicle = Vehicle_identification.objects.get(slug=slug)
        furniture_id = self.kwargs.get('pk')
        furniture = Furniture.objects.get(pk=furniture_id)
        if furniture.builder != self.request.user:
            raise PermissionDenied
        data = super(FurnitureEdit, self).get_context_data(**kwargs)
        data['projects'] = Project.objects.all()
        if self.request.POST:
            data['image_form'] = FurnitureFormset(self.request.POST)
        else:
            data['image_form'] = FurnitureFormset(instance=furniture)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        furniture_id = self.kwargs.get('pk')
        furniture = Furniture.objects.get(pk=furniture_id)
        vehicle = furniture.vehicle
        image_form = context['image_form']
        with transaction.atomic():
            form.instance.builder = self.request.user
            self.object = form.save()
            form.instance.vehicle = vehicle
            formset = FurnitureFormset(self.request.POST, self.request.FILES, instance = self.object)
            if formset.is_valid():
                for item in formset.cleaned_data:
                    if item:
                        if item['id']:
                            if item['DELETE']:
                                Furniture_pictures.objects.get(pk=number_extractor(item['id'])).delete()
                            else:
                                Furniture_pictures.objects.filter(pk=number_extractor(item['id'])).update(annotation=item['annotation'])
                        else:
                            image = item['image']
                            annotation = item['annotation']
                            photo = Furniture_pictures(parent=form.instance, image=image, annotation=annotation)
                            photo.save()

            if image_form.is_valid():
                image_form.instance = self.object
                image_form.save()
            return super(FurnitureEdit, self).form_valid(form)

    def get_success_url(self):
        furniture_id = self.kwargs.get('pk')
        furniture = Furniture.objects.get(pk=furniture_id)
        vehicle = furniture.vehicle
        slug = vehicle.slug
        return reverse('website:list_furniture', kwargs={'slug': slug})

class FurnitureDeleteView(SuccessMessageMixin, DeleteView):
    model = Furniture
    success_message = "Successfully deleted this record."
    template_name = "website/delete_confirmation.html"
    slug_for_redirect = None
    
    def get_slug(self, **kwargs):
        furniture_id = self.kwargs.get('pk')
        self.slug_for_redirect = Furniture.objects.get(id=furniture_id).vehicle.slug
    
    def get_queryset(self, **kwargs):
        self.get_slug(**kwargs)
        qs = super(FurnitureDeleteView, self).get_queryset()
        return qs.filter(builder=self.request.user)

    def get_context_data(self, **kwargs):
        data = super(FurnitureDeleteView, self).get_context_data(**kwargs)
        data['projects'] = Project.objects.all()
        return data

    def get_success_url(self, **kwargs):
        #furniture_id = self.kwargs.get('id')
        #vehicle_slug = Furniture.objects.get(pk=furniture_id).vehicle.slug
        return reverse_lazy( 'website:list_furniture',
        kwargs = {'slug': self.slug_for_redirect})

class VehicleDeleteView(SuccessMessageMixin, DeleteView):
    model = Vehicle_identification
    success_message = "Successfully deleted this record."
    template_name = "website/delete_confirmation.html"
    
    def get_queryset(self):
        qs = super(VehicleDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        data = super(VehicleDeleteView, self).get_context_data(**kwargs)
        data['projects'] = Project.objects.all()
        return data

    def get_success_url(self, **kwargs):
        slug = self.kwargs.get('slug')
        vehicle= Vehicle_identification.objects.get(slug=slug)
        project = Project.objects.get(name=vehicle.name)
        project.delete()
        return reverse_lazy('website:garage',
        kwargs = {'user': self.request.user})


class FurniturebyType(ListView):
    template_name = 'website/list_furniture.html'
    context_object_name = 'furniture_list'

    def get_queryset(self):
        type=self.kwargs.get('type')

        return Furniture.objects.filter(functionality=type).order_by('functionality')

    def number_of_likes(self):
        furniture_list = self.get_queryset()
        number_of_likes_dictionary = {}
        for item in furniture_list:
            number_of_likes_dictionary[item.pk]=item.post.count()
        return number_of_likes_dictionary

    def get_context_data(self):
        
        type=self.kwargs.get('type')
        image_list = Furniture_pictures.objects.filter(parent__functionality=type)
        context = super(FurniturebyType, self).get_context_data()
        context['image_list']=image_list
        context['projects'] = Project.objects.all()
        like_ref=self.number_of_likes()
        context['like_ref']=like_ref
        return context



class FurniturebyTechnique(ListView):
    template_name = 'website/list_furniture.html'
    context_object_name = 'furniture_list'

    def get_queryset(self):
        technique=self.kwargs.get('technique')
        return Furniture.objects.filter(build_techniques=technique).order_by('functionality')

    def number_of_likes(self):
        furniture_list = self.get_queryset()
        number_of_likes_dictionary = {}
        for item in furniture_list:
            number_of_likes_dictionary[item.pk]=item.post.count()
        return number_of_likes_dictionary

    def get_context_data(self, **kwargs):
        technique=self.kwargs.get('technique')        
        image_list = Furniture_pictures.objects.filter(parent__build_techniques=technique)
        context = super(FurniturebyTechnique, self).get_context_data(**kwargs)
        context['image_list']=image_list
        like_ref=self.number_of_likes()
        context['like_ref']=like_ref
        return context

class VehicleSearch(ListView):
    template_name = 'website/garage.html'
    model = Vehicle_pictures

    def number_of_likes(self, queryset):
        number_of_likes_dictionary = {}
        for item in queryset:
            number_of_likes_dictionary[item.pk]=item.post.count()
        return number_of_likes_dictionary
    

    def get_context_data(self, **kwargs):
        type = self.request.GET.get('type')
        technique = self.request.GET.get('technique')
        q = self.request.GET.get('q', False)
        if type=='none':
            type=False
        if technique=='none':
            technique=False
        has_parameters = False

        if type and not technique:
            has_parameters = True
            vehicle_list_tt = Vehicle_identification.objects.filter(project_base=type)
            image_list = Vehicle_pictures.objects.filter(parent__project_base=type)
            furniture_image_list = Furniture_pictures.objects.filter(parent__vehicle__project_base=type)
        if technique and not type:
            has_parameters = True
            vehicle_list_tt = Vehicle_identification.objects.filter(build_techniques=technique)
            image_list = Vehicle_pictures.objects.filter(parent__build_techniques=technique)
            furniture_image_list = Furniture_pictures.objects.filter(parent__vehicle__build_techniques=technique)
        if type and technique:
            has_parameters = True
            vehicle_list_tt = Vehicle_identification.objects.filter(project_base=type, build_techniques=technique)
            image_list = Vehicle_pictures.objects.filter(parent__project_base=type, parent__build_techniques=technique)
            furniture_image_list = Furniture_pictures.objects.filter(parent__vehicle__project_base=type, parent__vehicle__build_techniques=technique)
        if not type and not technique:
            vehicle_list_tt = None
            image_list = None
            furniture_image_list = None
        if q:
            # Filter q against vehicle fields
            vehicle_list1 = Vehicle_identification.objects.filter(
                Q(name__icontains=q) | Q(project_base__icontains=q) | Q(name__icontains=q) | Q(vehicle_description__icontains=q)
                )
            # Filter q against vehicle images
            vehicle_list_2 = Vehicle_identification.objects.filter(images__annotation__icontains=q)

            # Filter q against furniture images
            vehicle_list_3 = Vehicle_identification.objects.filter(
                Q(furnitures__description__icontains=q) | Q(furnitures__room__icontains=q)
                )
                
            # Filter q against vehicle images
            vehicle_list_4 = Vehicle_identification.objects.filter(furnitures__images__annotation__icontains=q)

            vehicle_list_search = vehicle_list1.union(vehicle_list_2, vehicle_list_3, vehicle_list_4)

            if has_parameters:
                vehicle_list=vehicle_list_tt.intersection(vehicle_list_search)
              
            if not has_parameters:
                vehicle_list = vehicle_list_search
                pks_in_vehicle_list = []
                for item in vehicle_list:
                    pks_in_vehicle_list.append(item.pk)
                image_list = Vehicle_pictures.objects.filter(parent__in=pks_in_vehicle_list)
                furniture_image_list = Furniture_pictures.objects.filter(parent__vehicle__in=pks_in_vehicle_list)

        if not q:
            vehicle_list = vehicle_list_tt
        context = {}
       # context = super(VehicleSearch, self).get_context_data(**kwargs)
        context['vehicle_list'] = vehicle_list
        context['image_list'] = image_list
        context['projects'] = Project.objects.all()
        context['furniture_image_list'] = furniture_image_list
        context['like_ref'] = self.number_of_likes(vehicle_list)
        return context


class FurniturebyBuilder(ListView):
    template_name = 'website/list_furniture.html'
    context_object_name = 'furniture_list'

    def get_queryset(self):
        builder_name=self.kwargs.get('builder')
        builder =  User.objects.get(username=builder_name)
        return Furniture.objects.filter(builder=builder).order_by('functionality')

    def number_of_likes(self):
        furniture_list = self.get_queryset()
        number_of_likes_dictionary = {}
        for item in furniture_list:
            number_of_likes_dictionary[item.pk]=item.post.count()
        return number_of_likes_dictionary

    def get_context_data(self, **kwargs):
        builder_name=self.kwargs.get('builder')
        builder =  User.objects.get(username=builder_name)        
        image_list = Furniture_pictures.objects.filter(parent__builder=builder)
        context = super(FurniturebyBuilder, self).get_context_data(**kwargs)
        context['image_list']=image_list
        like_ref=self.number_of_likes()
        context['like_ref']=like_ref
        context['projects'] = Project.objects.all()
        return context


def like(request):
    data = json.loads(request.body)
    pk = data.get('pk')
    try:
        previous_like = Furniture_likes.objects.filter(user=request.user).get(post_id=pk)
    except:
        previous_like = False

    if previous_like:
        return JsonResponse({"already_liked": True}, status=404)
    elif not previous_like:
        like_instance = Furniture_likes(user=request.user, post=Furniture.objects.get(pk=pk))
        like_instance.save()
    
    new_like_count = Furniture.objects.get(pk=pk).post.count()

    return JsonResponse({"already_liked": False, "new_like_count": new_like_count}, status=201)
    

def vehlike(request):
    data = json.loads(request.body)
    pk = data.get('pk')
    try:
        previous_like = Vehicle_likes.objects.filter(user=request.user).get(post_id=pk)
    except:
        previous_like = False

    if previous_like:
        return JsonResponse({"already_liked": True}, status=404)
    elif not previous_like:
        like_instance = Vehicle_likes(user=request.user, post=Vehicle_identification.objects.get(pk=pk))
        like_instance.save()
    
    new_like_count = Vehicle_identification.objects.get(pk=pk).post.count()

    vehicle_name = Vehicle_identification.objects.get(pk=pk).name
    placeOnTree = Project.objects.get(name=vehicle_name)
    placeOnTree.like_count = new_like_count
    placeOnTree.save()

    return JsonResponse({"already_liked": False, "new_like_count": new_like_count}, status=201)
    



def deletemessage(request):
    data = json.loads(request.body)
    pk = data.get('pk')
    message_object = Message.objects.get(pk=pk)
    if message_object.sender != request.user and message_object.recipient != request.user:
        raise PermissionDenied

    message_object.delete()
    return JsonResponse({"deleted": True}, status=201)

       
def projectpreview(request):
    data = json.loads(request.body)
    name = data.get('name')

    #first exterior image
    exterior_image = Vehicle_pictures.objects.filter(parent__name=name).first()


    #vehicle information
    object = Vehicle_identification.objects.get(slug=slugify(name))

    #create context
    context = {}
    context['exterior_image'] = image_path(exterior_image.image.path)
    context['owner'] = object.owner.username
    context['description'] = object.vehicle_description
    data = json.dumps(context, default=vars)
    return JsonResponse(data, status=201, safe=False)

def build(request, name):
    pass


class VehicleDetailView(DetailView):
    template_name = 'website/projects.html'
    model = Vehicle_identification
    
    def number_of_likes(self):
        
        #update view count
        vehicle = self.get_object()
        vehicle.view_count += 1
        vehicle.save()


        list = self.get_queryset()
        number_of_likes_dictionary = {}
        for item in list:
            number_of_likes_dictionary[item.pk]=item.post.count()
        return number_of_likes_dictionary

    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        image_list = Vehicle_pictures.objects.filter(parent__slug=slug)
        context = super(VehicleDetailView, self).get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        context['image_list'] = image_list
        self.this_vehicle = Vehicle_identification.objects.get(slug=slug)
        context['furniture'] = Furniture.objects.filter(vehicle=self.this_vehicle).order_by('room')
        context['room_pics'] = Furniture_pictures.objects.filter(parent__vehicle=self.this_vehicle)
        context['like_ref'] = self.number_of_likes()
        context['comments'] = self.get_object().comments.filter(active=True)
        context['comment_form'] = CommentForm()
        return context

class VehicleCommentView(SingleObjectMixin, FormView):
    template_name = 'website/project.html'
    model = Vehicle_identification
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Unsuccessful post. Login required.")
            return HttpResponseRedirect(self.request.path_info)
            
        self.object = self.get_object()
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.vehicle = self.object
            new_comment.name = request.user
            new_comment.save()
            new_comment.image = request.FILES.get('image', None)
            messages.info(request, "Post was successful.")
            return HttpResponseRedirect(self.request.path_info)
   # def get_success_url(self):
   #     return reverse('website:vehicle', kwargs={'slug':self.object.slug})

class VehicleView(View):
    
    def get(self, request, *args, **kwargs):
        view = VehicleDetailView.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = VehicleCommentView.as_view()
        return view(request, *args, **kwargs)


def reply_page(request):
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle_id = request.POST.get('vehicle_id')
            parent_id = request.POST.get('parent')
            current_url = request.POST.get('current_url')
            reply = form.save(commit=False)
            reply.vehicle = Vehicle_identification.objects.get(pk=vehicle_id)
            reply.parent = Comment(id=parent_id)
            reply.name = request.user
            reply.save()
            slug = Vehicle_identification.objects.get(pk=vehicle_id).slug
            return HttpResponseRedirect(current_url)
    return HttpResponseRedirect(request.path_info)