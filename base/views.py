from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from pyrsistent import b
from users.models import MyUser
from django.contrib.auth.decorators import login_required
from .models import Book,Contact,Order,Rating
from django.contrib import messages
import pandas as pd
import numpy as np
from datetime import datetime,date
from django.core.paginator import Paginator
from .UserBasedCF import UserBasedCollaborativeFiltering

@login_required
def kryefaqja(request):
    #leximi i te dhenave
    total=Book.objects.all().count()
    books = pd.DataFrame(list(Book.objects.all().values()))
    ratings=pd.DataFrame(list(Rating.objects.all().values()))


    #bashkimi sipas ISBN
    book_rating = ratings.join(books.set_index('ISBN'), on='book_isbn_id')
    #shtimi i nje kolone ne dataframe qe ruan numrin e vlersimeve per liber 
    book_rating['count']= book_rating.groupby(['book_title'])['rating'].transform('count')
    #shtimi i nje kolone ne dataframe qe ruan vleren e mesatares se vleresimeve
    book_rating['mean']=book_rating[book_rating['count']>20].groupby('book_title')['rating'].transform('mean')
    #renditja sipas mesatares
    top_books=book_rating.sort_values(by=['mean'], ascending=[False])
    #fshirja e perseritjeve
    top_books=top_books.drop_duplicates(subset='book_title')
    top_books.drop(['rating','user_id_id','id'], inplace=True, axis=1)
    top_books.columns=['isbn','title','author','yop','puplisher','image_url','count','mean']


    #konvertimi ne list(vektor)
    top_books=top_books.values.tolist()

    book_paginator = Paginator(top_books, 10)
    if(request.GET.get('page')==None ):
        page_num=1
    else:
        page_num=request.GET.get('page')

    page = book_paginator.get_page(page_num)
    r=range(page.number,page.number+5)

    context={'page':page,'range':r,'total':total}
    return render(request,'kryefaqja.html',context)


@login_required
def profili(request):
    user=request.user
    orders=Order.objects.filter(user_id=user)
    data=date.today()

    context={'orders':orders,'user':user,"data":data}
    return render(request,'profili.html',context)



@login_required
def kontakt(request):
    user=request.user
    if request.method == 'POST': 
            name = request.POST['name']
            email = request.POST['email']
            subject = request.POST['subject']
            message = request.POST['message']
            if name=="" or email=="" or message=="":
                return redirect('kontakt')
            else:
                contact=Contact.objects.create(name=name,email=email,subject=subject,message=message,date_sended=datetime.now(),user_id=user)
                contact.save()
                return redirect('kryefaqja') 
    else:
        return render(request,'kontakt.html')


@login_required
def librat(request):
    publishersBook=Book.objects.values('publisher', 'ISBN')
    publishers= [item["publisher"] for item in publishersBook] #grumbullimi i infos per shtepite botuese
    publishers=list( dict.fromkeys(publishers))#fshirja e perseritjeve
    allBooks=[]
    #cikel qe kategorizon librat sipas shtepive botuese
    for publisher in publishers:
        books=Book.objects.filter(publisher=publisher)
        allBooks.append(books)

    book_paginator = Paginator(allBooks,6)
    if(request.GET.get('page')==None ):
        page_num=1
    else:
        page_num=request.GET.get('page')

    page = book_paginator.get_page(page_num)
    r=range(page.number,page.number+5)

    context={'page':page,'range':r}
    return render(request,'librat.html',context) #dhenia e aksesit te te dhenave per tu shfaqur ne frontend


def search(request):
    if request.method == 'POST':
        searched=request.POST['searched']
        if len(searched)>3:
            searched=request.POST['searched']
            books=Book.objects.filter(book_title__icontains=searched)
            context={'librat':books,'kerkim':searched}
            return render(request,'search.html',context)
        else:
            return redirect('kryefaqja')
    else:
        return redirect('kryefaqja')


@login_required
def liber(request,pk):
    liber=Book.objects.get(ISBN=pk)
    sot=date.today().strftime('%Y-%m-%d')

    user=request.user
    liber=Book.objects.get(ISBN=pk)

    if request.method == 'POST': 
        if 'orderS' in request.POST:
            date_s = request.POST['date_s']
            date_e = request.POST['date_e']
            order=Order.objects.create(date_s=date_s,date_e=date_e,confirmed=False,book_isbn=liber,user_id=user)
            order.save()
            return redirect('kryefaqja') 
        if 'ratingS' in request.POST:
            r=request.POST['rating']
            rating=Rating.objects.create(rating=r,book_isbn=liber,user_id=user)
            rating.save()
            return redirect('kryefaqja') 
    else:
        context={'liber':liber,'day':sot}
        return render(request,'liber.html',context)



@login_required
def dil(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')

@login_required
def rekomandimet(request):
    user_id=request.user.id
    if(Rating.objects.filter(user_id=user_id)):
        ratings=pd.DataFrame(list(Rating.objects.all().values()))
        users=pd.DataFrame(list(MyUser.objects.all().values()))
        books = pd.DataFrame(list(Book.objects.all().values()))
        ratings.drop('id', axis=1, inplace=True)
        ratings.columns=["bookRating","userId","ISBN"]


        book_ratings = ratings.pivot_table(index='userId', columns='ISBN', values='bookRating').fillna(0) 
        user_r_list = book_ratings.index.tolist()
        sampled_users = users.loc[users['id'].isin(user_r_list)]
        sampled_users = sampled_users.reset_index()
        sampled_users = sampled_users.drop(['index'], axis=1) 
        book_r_list = book_ratings.columns.values.tolist()
        sampled_books = books.loc[books['ISBN'].isin(book_r_list)]
        sampled_books = sampled_books.reset_index()
        sampled_books = sampled_books.drop(['index'], axis=1) 
        user_based_cf = UserBasedCollaborativeFiltering(sampled_users, sampled_books, book_ratings)
        recommendations = user_based_cf.recommend(user_id) 
        recommendations=recommendations.values.tolist()
        recommendations=recommendations[0:10]
        
    else:
        recommendations=[]
        print("Nuk ka vlersime")
    
    context={"rekomandimet":recommendations}
    return render(request,'rekomandimet.html',context)





