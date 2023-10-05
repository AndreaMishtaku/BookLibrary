from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
import pandas as pd
from .models import MyUser
from .forms import LoginForm,SignUpForm


def identifikohu(request):
    if not request.user.is_authenticated:
        error_message=[]
        if request.method == 'POST': 
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)

            if '@' not in email:
                error_message.append("Email jo i sakte!")
            if len(password)<6:
                error_message.append("Password duhet te jete me i gjate se 6!")
            if user is None or email == 'andrea@gmail.com':
                error_message.append("Perdoruesi nuk egziston!")


            
            if len(error_message)==0:
                login(request, user)
                return redirect('kryefaqja')
            else:
                context={"errors":error_message}
                return render(request,'identifikohu.html',context) 
        else:
            context={"errors":error_message}
            return render(request,'identifikohu.html',context)
    else:
        return redirect('kryefaqja')

        
    
def regjistrohu(request):
    if not request.user.is_authenticated:
        error_message=[]
        if request.method == 'POST':
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            gender= request.POST['gender']
            email= request.POST['email']
            phone= request.POST['phone']
            password = request.POST['password']
            age= request.POST['age']
            city= request.POST['city']
            state=request.POST['state']
            country=request.POST['country']


            if  MyUser.objects.filter(email=email).exists():
                error_message.append("Ky email eshte i regjistruar!")
            if '@' not in email:
                error_message.append("Email jo i sakte!")
            if len(password)<6:
                error_message.append("Password duhet te jete me i gjate se 6!")


            if  len(error_message)>0:
                context={"errors":error_message}
                return render(request,'regjistrohu.html',context)  
            else:
                user = MyUser.objects.create_user(firstname=firstname,lastname=lastname,gender=gender,email=email,phone=phone,password=password,age=age,city=city,state=state,country=country)
                user.save()
                request.session["firstname"]=firstname
                request.session["lastname"]=lastname
                print('Accounti i perdoruesit u krijua')
                return redirect('identifikohu')
        else:
            context={"errors":error_message}
            return render(request,'regjistrohu.html',context)
    else:
        return redirect('kryefaqja')




