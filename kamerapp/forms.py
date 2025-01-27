from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['image_user', 'tel', 'sexe', 'langue']
