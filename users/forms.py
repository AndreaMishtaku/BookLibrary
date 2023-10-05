from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import MyUser
import re

class SignUpForm(UserCreationForm):
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta(UserCreationForm):
        model = MyUser
        fields = ('firstname','lastname','gender','age','email','phone','city','state','country')
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }

class LoginForm(AuthenticationForm):
    email=forms.CharField(label='Email',widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=MyUser
        fields=['email','password']
        labels={'email':'Email','password':'Password'}

    def clean_email(self,*args,**kwargs):
        email=self.cleaned_data.get("email")
        if  re.match('\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', email) != None:
            return email
        else:
            raise forms.ValidationError("Email jo i sakte")

    def clean_password(self,*args,**kwargs):
        password=self.cleaned_data.get("password")
        if  len(password)>=6:
            return password
        else:
            raise forms.ValidationError("Password duhet te jete me i gjete se 6 karaktere")

