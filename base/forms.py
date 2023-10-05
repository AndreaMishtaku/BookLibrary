from django import forms
from datetime import timedelta

class orderForm(forms.Form):
    date_s = forms.CharField(required=True,label='',widget=forms.DateInput(attrs={'class':'form-control','type':'date','style':'width:40%'}))
    date_e = forms.CharField(required=True,label='',widget=forms.DateInput(attrs={'class':'form-control','type':'date','style':'width:40%'}))
   

class ratingForm(forms.Form):
    rating=forms.CharField(required=True,label='',widget=forms.NumberInput(attrs={'class':'form-control','type':'number','value':'1','min':'1','max':'10','style':'width:40%'}))
