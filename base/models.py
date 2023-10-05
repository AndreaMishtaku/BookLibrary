from django.db import models
from numpy import False_
from users.models import MyUser
class Book(models.Model):
    ISBN=models.CharField(max_length=70,primary_key=True)
    book_title=models.CharField(max_length=255)
    book_author=models.CharField(max_length=150)
    year_of_publication=models.IntegerField()
    publisher=models.CharField(max_length=100)
    image_url=models.CharField(max_length=150)
    def __str__(self):
        return str(self.pk)

class Rating(models.Model):
    id=models.AutoField(primary_key=True)
    rating=models.IntegerField()
    user_id=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    book_isbn=models.ForeignKey(Book,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)

class Contact(models.Model):
    id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    subject=models.CharField(max_length=100)
    message=models.TextField(max_length=500)
    date_sended=models.DateTimeField()

    def __str__(self):
        return str(self.pk)

class Order(models.Model):
    id=models.AutoField(primary_key=True)
    date_s=models.DateField()
    date_e=models.DateField()
    confirmed=models.BooleanField(default=False)
    user_id=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    book_isbn=models.ForeignKey(Book,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.pk)