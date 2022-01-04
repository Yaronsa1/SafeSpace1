from django.db import models
from django.forms import ModelForm
from base.models import Place,User
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1','password2']

class PlaceForm(ModelForm):
    class Meta:
        model = Place
        fields = '__all__'
        exclude = ['owner']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username','email','avatar', 'greenpass']

