from django import forms
from shop.models import *

class CustomUserForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Name','class':'form-control'}))
    email=forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Enter Email','class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password','class':'form-control'}))
    
    
    class Meta:
        model=CustomUser
        fields=['name','email','password']

    

        
class ProfileUserForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['profile_pic']
