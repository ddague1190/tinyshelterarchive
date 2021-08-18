from typing import Collection 
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *
from django_bleach.forms import BleachField
from mptt.forms import TreeNodeChoiceField, TreeNodePositionField

class AddFurnitureForm(forms.ModelForm):
    class Meta:
        model = Furniture
        exclude = ('builder', 'vehicle')
        #fields = "__all__"

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'profile_pic', 'website', )

    bio = BleachField()

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")
      
# ***** Create a new vehicle *****     

class Vehicle_picturesForm(forms.ModelForm):
    class Meta:
        model = Vehicle_pictures
        fields = ('image', 'annotation')
        # exclude = ()

Vehicle_picturesFormset = inlineformset_factory(Vehicle_identification, Vehicle_pictures,
    form = Vehicle_picturesForm, fields=['image', 'annotation'], extra=1, can_delete=True, max_num=21)

class Vehicle_identificationForm(forms.ModelForm):

    queryset=Project.objects.filter(tree_linked=False, can_be_parent = True)
    project_base = TreeNodeChoiceField(queryset, level_indicator='--')
    
    vehicle_description = BleachField(allowed_tags=[
        'p', 'b', 'i', 'u', 'em', 'strong', 'a',
        'img', 'h3', 'h4', 'h5', 'h6'])

    class Meta:
        model = Vehicle_identification
        fields = ['project_base', 'vehicle_description', 'name', 'build_techniques']


    def __init__(self, *args, **kwargs): 
        super(Vehicle_identificationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form_horizontal'
        # self.helper.label_class = 'testy'
        # self.helper.field_class = 'testy2'
        self.helper.attrs = {'enctype':"multipart/form-data"}
    
        self.helper.layout = Layout(

            Div(
                Field('name'),
                Field('project_base'),
                Field('build_techniques'),
                Field('vehicle_description'),
                Fieldset('Pictures of exterior (up to 21)',
                    Formset('image_form')),
                HTML('<br>'),
                ButtonHolder(Submit('submit', 'save')),
            )


            )

# ***** Build new furniture *****     


class Furniture_picturesForm(forms.ModelForm):
    class Meta:
        model = Furniture_pictures
        fields = ('image', 'annotation', )

FurnitureFormset = inlineformset_factory(Furniture, Furniture_pictures,
    form = Furniture_picturesForm, fields=['image', 'annotation'], extra=1, can_delete=True, max_num=21)

class FurnitureForm(forms.ModelForm):
    class Meta:
        model = Furniture
        exclude = ['builder', 'vehicle', ]

    def __init__(self, *args, **kwargs): 
        super(FurnitureForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form_horizontal'
       # self.helper.label_class = 'col-md-3 create-label'
        #self.helper.field_class = ''
        self.helper.attrs = {'enctype':"multipart/form-data"}
    
        self.helper.layout = Layout(

            Div(
                Field('room'),
                Field('description'),
                Field('functionality'),
                Fieldset('Add images (up to 21)',
                    Formset('image_form')),
                HTML('<br>'),
                ButtonHolder(Submit('submit', 'save')),
            )


            )


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('subject', 'message', )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', 'image')

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs = {'placeholder': 'Comment here...', 'class':'form-control', 'rows':'2'}
