from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils.translation import gettext_lazy as _



class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email,password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email,password, **other_fields)

    def create_user(self, email,password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email,**other_fields)
        user.set_password(password)
        user.save()
        return user




class MyUser(AbstractBaseUser,PermissionsMixin):
    id = models.AutoField(primary_key=True)
    firstname= models.CharField(max_length=30)
    lastname= models.CharField(max_length=30)
    gender= models.CharField(max_length=30)
    email = models.EmailField(_('email address'), unique=True)
    phone=models.CharField(max_length=15) 
    password=models.CharField(max_length=255) 
    age = models.FloatField(null=True)
    city=models.CharField(max_length=150)
    state=models.CharField(max_length=150)
    country=models.CharField(max_length=150)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)


    objects = CustomAccountManager()


    USERNAME_FIELD='email'

    def __str__(self):
        return str(self.pk)
